#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 16:35:06 2019

@author: AlexYeeeeee
"""
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


def getFiles():
    filePath = 'University of California, Riverside Home.html'
    #files = sorted(glob.glob(filePath))
    #for html in files:
        #htmlParse(html)
    htmlParse(filePath)

def htmlParse(fileToParse):
    soup = BeautifulSoup(open(fileToParse),'lxml')
    
    #Get title works correctly
    web_title = soup.find('title').get_text()
    
    #Get body works correctly 
    tempBody = []
    for sentences in soup.find_all('p'):
        tempBody.append(sentences.getText())
        
    body = ''.join(str(word) for word in tempBody)
   
    #Get URL not working currently 
    for url in soup.find('line'):
        print(url.get('href'))
        #web_url = url
    
        
'''   
    print()
    print()
    print('{' + '\n')
    print(' ' + '"' + 'web_title' + '"' + ' = ' + web_title)
    print()
    print(' ' + '"' + 'web_url' + '"' + ' = ' + web_url)
    print()
    print(' ' + '"' + 'body' + '"' + ' = ' + body)
    print()
    print('}' + '\n')
'''   
    
    
getFiles()