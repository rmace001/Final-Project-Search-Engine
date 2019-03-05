from bs4 import BeautifulSoup as bs
import urllib.request
import csv
import os
from hurry.filesize import size
import re
from pyspark import SparkContext
import time
import threading
import concurrent.futures
from urllib import request

total_memory = 0
MAX_MEMORY = 1.5*1024*10**6 # 1GB 1024*10**6 only 976

def main():
    NUM_WORKERS = 16
    global MAX_MEMORY
    global total_memory

    urlpage = 'https://www.ucr.edu/'
    total_link_list = []
    total_link_list.append(urlpage)
    level = 1 
    link_index = {} # { html: level }
    link_index[urlpage] = level

    new_link = [] 
    index = 0
    for i in range(len(total_link_list)):
        link_item =  total_link_list.pop(0)
        next_level, link_index = search_download(link_item, level, link_index,1)
        new_link += next_level
    print(new_link)
    
    total_link_list += list(set().union(new_link))

    for i in range (2):
        new_link.clear()
        level += 1
        with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
            futures = {executor.submit(search_download, address, level, link_index,total_link_list.index(address)+1) for address in total_link_list}
            concurrent.futures.wait(futures)
            for item in futures:
                new_link += item.result()[0]
                link_index = item.result()[1]
        total_link_list.clear()
        total_link_list += list(set().union(new_link))
    print(total_link_list)
    print(total_memory)
    print(link_index)

def search_download (urlpage,level,link_index,page):
    global total_memory 
    list_link = []
    headers = {'User-Agent':'Mozilla/5.0'}
    # build the header/user-agent to deal with webPAGE 403
    req = urllib.request.Request(url=urlpage, headers=headers)
    try:    
        soup = bs(urllib.request.urlopen(req),'html.parser')
    except urllib.error.URLError as error:
        print (error)
        return list_link, link_index
    html = soup.prettify()
    filename = "web_" + str(level) + "_" + str(page)
    with open('data/' + filename, "w") as f:
        print(html,file = f)
    f.close()

    memory =  os.stat('data/' + filename)
    total_memory += memory.st_size
    print(size(total_memory)+ " data/" + filename)
    
    
    level += 1
    for link in soup.find_all('a'):
        link_name = link.get('href')
        if(link_name):
            if link_name.startswith("http"):
                if link_name.endswith(".edu") or link_name.endswith(".edu/"):
                    if link_name not in link_index:
                        list_link.append(link_name) 
                        link_index[link_name] = level
    list_link = list(set().union(list_link))

    return list_link, link_index
# main function

start = time.time()
main()
end = time.time()
print(end - start)

