import string
import os
import glob
import numpy as np
import pandas as pd
import math
#For processing file in particular format based off of <doc>/<DOCNO>
from bs4 import BeautifulSoup
#For stemming
from nltk.stem import PorterStemmer
#For use of tokenizing to be applied with stemming (NOT USED)
from nltk.tokenize import word_tokenize
import operator
import urllib.request
import re
import json
def htmlParse(newdirectory, filename, level, page_number):


    #Start the soup
    soup = BeautifulSoup(open(newdirectory+ "/"+ filename),'lxml')

    #Get URL
    file_open =  open(newdirectory+ "/" + filename, 'r') 
    web_url = file_open.readline() 
    web_url = web_url.replace("\n","")

    #Get title works correctly
    try:
        web_title = soup.find('title').get_text()
        web_title = web_title.replace("\n", "")
        web_title = re.sub(" +",' ', web_title)
    except:
        web_title = ""
    
    #Get body works correctly
    tempBody = []
    for sentences in soup.find_all('p'):
        tempBody.append(sentences.getText())

    #Pop the source URL before converting to string
    tempBody.pop(0)
    body = ''.join(str(word) for word in tempBody)
    body = body.replace("\n", "")
    body = re.sub(' +', ' ', body)
    data = {}
    data['create'] = { "_index": "webdocs", "_type": "webdoc", "_id": str(page_number)}
    item  = {}
    item = {"id" : str(page_number), "title" :web_title, "url" :web_url, "level": level, "body": body}
    with open('data.txt', 'a') as file_out:
        json.dump(data,file_out)
        file_out.write("\n")
        json.dump(item,file_out)
        file_out.write("\n")

directory = 'data_1/'
count  = 0
for i in range(1, len(os.listdir(directory))+1):
    newdirectory =  directory + "level" +str(i) 
    for filename in os.listdir(newdirectory):
        count += 1
        htmlParse(newdirectory, filename, i, count)


#getFiles()










