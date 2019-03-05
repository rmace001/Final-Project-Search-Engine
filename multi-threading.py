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

total_memory = 0
MAX_MEMORY = 1.5*1024*10**6 # 1GB 1024*10**6 only 976
def main():
    NUM_WORKERS = 4
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
        next_level, link_index = search_download(link_item, 2, link_index,index)
        new_link += next_level
    print(new_link)
    #print("total_link_list" ,total_link_list)
    total_link_list += list(set().union(new_link))
    print("total_link_list have ", total_link_list)
    
    new_link.clear()
    print("here is link index", link_index)
    print("len is ", len(link_index))
    with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
        futures = {executor.submit(search_download, address, 3, link_index,index) for address in total_link_list}
        concurrent.futures.wait(futures)
        for item in futures:
            new_link += item.result()[0]
            link_index = item.result()[1]

    new_link = list(set().union(new_link))
    print("here is link index", link_index)
    print("len is ", len(link_index))
    print("new_link ", new_link)
    print("len is ", len(new_link))
    print(total_memory)

def search_download (urlpage,level,link_index,index):
    global total_memory
    global total_queue
    headers = {'User-Agent':'Mozilla/5.0'}
    # build the header/user-agent to deal with webPAGE 403
    req = urllib.request.Request(url=urlpage, headers=headers)

    soup = bs(urllib.request.urlopen(req),'html.parser')
    html = soup.prettify()
    filename = "web_" + str(level) + "_" + str(index)
    with open('data/' + filename, "w") as f:
        print(html,file = f)
    f.close()
    memory =  os.stat('data/' + filename)
    total_memory += memory.st_size
    print(size(total_memory))
    #print(size(10**9)) # 953
    #print(size(1024*10**6)) #976
    list_link = []
    

    for link in soup.find_all('a'):
        link_name = link.get('href')
        if(link_name):
            if link_name.startswith("http"):
                if link_name.endswith(".edu") or link_name.endswith(".edu/"):
                    if link_name not in link_index:
                        list_link.append(link_name) 
                        link_index[link_name] = level
    list_link = list(set().union(list_link))
    #print(list_link)
    #print(len(list_link)) 35
    #print(link_index)
    #print(len(link_index)) 36
    return list_link, link_index
# main function

start = time.time()
main()
end = time.time()
print(end - start)

