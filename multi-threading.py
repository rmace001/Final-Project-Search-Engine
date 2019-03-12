from bs4 import BeautifulSoup as bs
import urllib.request
import csv
import os
from hurry.filesize import size
import re
import time
import concurrent.futures
from urllib import request
import socket
total_page = 0
total_memory = 0
MAX_MEMORY = 1024*(10**6) # 1GB 1024*10**6 only 976
def remove(urlpage):
    text = re.sub(r'^(http)?s?:?//(www.)? *', '', urlpage, flags=re.MULTILINE) 
    page_name = re.sub(r'.edu/?$', '', text, flags=re.MULTILINE) 
    return page_name

def create_url(page_name):
    return 'https://www.' + page_name + ".edu"

def main(limit_bool,limit_level_int,limit_page_int):
    NUM_WORKERS = 16
    global MAX_MEMORY
    global total_memory
    global total_page
    urlpage = 'https://www.ucr.edu/'
    total_link_list = []
    total_link_list.append(urlpage)
    level = 1 
    link_index = {} # { html: level }
    link_index[remove(urlpage)] = level

    new_link = [] 
    index = 0
    os.makedirs('data/'+ 'level' +str(level)+"/")
    total_page = len(link_index)
    print("Now total page is ",total_page)
    for i in range(len(total_link_list)):
        link_item =  total_link_list.pop(0)
        next_level, link_index = search_download(link_item, level, link_index,1,True)
        new_link += next_level

    total_link_list += list(set().union(new_link))
    not_over_limit  = True
    diff = int(limit_page_int) - total_page 
    #print("diff is ", diff)
    if diff < len(total_link_list):
        total_link_list =   total_link_list[:(diff)]
        print("NOW next level is ", len(total_link_list))
    while not_over_limit:
        new_link.clear()
        level += 1
        if total_memory < MAX_MEMORY :
            os.makedirs('data/'+ 'level' +str(level)+"/")
        with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
            futures = {executor.submit(search_download, address, level, link_index,total_link_list.index(address)+1,not_over_limit) for address in total_link_list}
            concurrent.futures.wait(futures)
            for item in futures:
                new_link += item.result()[0]
                link_index = item.result()[1]

        print("now it is total_page is ", len(link_index))
        if (limit_bool): # if limit = true check the level to MAX level
            if (limit_level_int == level):
                print("LightSABR's web crawling reach level: ", level)
                not_over_limit = False
            if total_page == limit_page_int:
                not_over_limit = False
        if total_memory > MAX_MEMORY :
            not_over_limit = False
        if not_over_limit :
            total_link_list.clear()
            total_link_list += list(set().union(new_link))
            #print("total_memory now is: ", size(total_memory))
    print("LightSABR's web crawling reach memory: ", total_memory)
    print("LightSABR's web crawling reach page: ", total_page)


def search_download (urlpage,level,link_index,page,not_over_limit):
    global total_memory 
    list_link = []
    global total_page
    # build the header/user-agent to deal with webPAGE 403
    headers = {'User-Agent':'Mozilla/5.0'}
    # check URL error 
    if urlpage.startswith("https//"):
        urlpage = urlpage.replace("https//" , "https://")
    if urlpage.startswith("http//"):
        urlpage = urlpage.replace("http//" , "https://")
    try:    
        req = urllib.request.Request(url=urlpage, headers=headers)
        soup = bs(urllib.request.urlopen(req,timeout = 10),'html.parser')
    except:
        return list_link, link_index  
    # end of check URL error
    # load the file  
    html = soup.prettify()
    filename = "web_" + str(page)
    try:
        if not_over_limit :
            with open('data/'+ 'level' +str(level)+"/" + filename, "w") as f:
                f.write(urlpage)
                f.write("\n")
                print(html,file = f)
            f.close()
    except:
        return list_link, link_index
    # end of load file
    # check memory
    memory =  os.stat('data/'+ 'level' +str(level)+"/" + filename)
    total_memory += memory.st_size
    # end of check memory
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
if __name__ == "__main__":
    os.makedirs("data/")
    print("\n***************************************************************")
    print("Weclome to LightSABR's web crawling\n")
    print("Default: : if application get the file over 1GB in level K, the application will stop when it finished web crawling in level K")
    print("Do you want to limit the web crawl by page or level ?")
    answer = input("1 for yes OR 0 for No : ")

    limit_level = 0
    limit_page = 0
    limit_memory = 0
    limit = True
    if answer == '0':
        limit = False
    if answer == '1':
        limit = True
        print("If you want to limit by level or page, the application wouldn't limit by 1 GB")
        limit_level = int(input("Please enter MAX ( input must >1 ) level = "))
        limit_page = int(input("Please enter MAX ( input must >1 ) page = "))
        print("\n==============================================================================\n")
    start = time.time()
    main(limit,limit_level,limit_page)
    end = time.time()
    print("LightSABR's web crawling spend :", end - start)
   