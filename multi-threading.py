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
from http.client import IncompleteRead
import socket

total_memory = 0
MAX_MEMORY = 1.5*1024*(10**6) # 1GB 1024*10**6 only 976
def remove(urlpage):
    text = re.sub(r'^(http)?s?:?//(www.)? *', '', urlpage, flags=re.MULTILINE) 
    page_name = re.sub(r'.edu/?$', '', text, flags=re.MULTILINE) 
    return page_name

def create_url(page_name):
    return 'https://' + page_name + ".edu"

def main():
    NUM_WORKERS = 16
    global MAX_MEMORY
    global total_memory

    urlpage = 'https://www.ucr.edu/'
    total_link_list = []
    total_link_list.append(urlpage)
    level = 1 
    link_index = {} # { html: level }
    link_index[remove(urlpage)] = level

    new_link = [] 
    index = 0
    for i in range(len(total_link_list)):
        link_item =  total_link_list.pop(0)
        next_level, link_index = search_download(link_item, level, link_index,1,True)
        new_link += next_level
    #print(new_link)
    
    total_link_list += list(set().union(new_link))
    not_over_limit  = True
    while not_over_limit:
        pass
        new_link.clear()
        level += 1
        with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
            futures = {executor.submit(search_download, address, level, link_index,total_link_list.index(address)+1,not_over_limit) for address in total_link_list}
            concurrent.futures.wait(futures)
            for item in futures:
                new_link += item.result()[0]
                link_index = item.result()[1]
        total_link_list.clear()
        total_link_list += list(set().union(new_link))
        #print(size(total_memory))
        if total_memory > MAX_MEMORY :
            not_over_limit = False

    #print(total_link_list)
    with open('total_index' + filename, "w") as f:
        print(link_index,file = f)
    #print(link_index)
    print(total_memory)

def search_download (urlpage,level,link_index,page,not_over_limit):
    global total_memory 
    list_link = []

    # build the header/user-agent to deal with webPAGE 403
    headers = {'User-Agent':'Mozilla/5.0'}
    
    # check URL error 
    if urlpage.startswith("https//"):
        urlpage = urlpage.replace("https//" , "https://")
    if urlpage.startswith("http//"):
        urlpage = urlpage.replace("http//" , "https://")
    try:    
        req = urllib.request.Request(url=urlpage, headers=headers)
        soup = bs(urllib.request.urlopen(req,timeout = 20),'html.parser')
    except urllib.error.URLError as error:
        #print (error)
        return list_link, link_index
    except IncompleteRead:
    # Oh well, reconnect and keep trucking
        #continue 
        return list_link, link_index
    except socket.error:
        return list_link, link_index
    except:
        return list_link, link_index

    html = soup.prettify()
    filename = "web_" + str(page)
    with open('data/'+ 'level' +str(level)+"/" + filename, "w") as f:
        print(html,file = f)
    f.close()

    memory =  os.stat('data/'+ 'level' +str(level)+"/" + filename)
    total_memory += memory.st_size
    #print("data_1/" + filename)
    
    if not_over_limit :
        level += 1
        for link in soup.find_all('a'):
            link_name = link.get('href')
            if(link_name):
                if link_name.startswith("http"):
                    if link_name.endswith(".edu") or link_name.endswith(".edu/"):
                        s1 = remove(link_name) 
                        if s1 not in link_index:
                            if link_name.startswith("https//"):
                                link_name = link_name.replace("https//" , "https://")
                            if link_name.startswith("http//"):
                                link_name = link_name.replace("http//" , "https://")

                            list_link.append(link_name)
                            link_index[s1] = level
        list_link = list(set().union(list_link))

    return list_link, link_index
# main function

start = time.time()
main()
end = time.time()
print(end - start)

