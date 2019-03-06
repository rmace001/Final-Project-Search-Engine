#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 14:30:37 2019

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

"""
def getFiles():
    filePath = 'data/*.html'
    files = sorted(glob.glob(filePath))
    for html in files:
        htmlParse(html)

def htmlParse(fileToParse):
    soup = BeautifulSoup(open(fileToParse),"html.parser")
    for line :

#def htmlParse():        
"""



#------------------------------------------------------------------------------------------
#Get Title 
#sauce = urllib.request.urlopen('https://pythonprogramming.net/parsememcparseface/').read()
#Set the url, send request
sauce = urllib.request.urlopen('https://ucr.edu').read()
soup = BeautifulSoup(sauce, 'lxml')
#Below can also be used
#soup = BeautifulSoup(sauce, 'html.parser')

#print(soup.title)

#soup.title.string gives us the web title from the URL, .string gives us the string 
#instead of html formatted title
print(soup.title.string)
print()

#Assign title to web_title variable
web_title = soup.title.string
#------------------------------------------------------------------------------------------
#Get Body
tempBody = []

#Find body tags to get all bodies of text, append to tempBody list
for sentences in soup.find_all('p'):
    #Line below creates list with str objects for each body
    tempBody.append(sentences.getText())

#Converts tempBody list into 1 string
body = ''.join(str(word) for word in tempBody)
print(body)
#------------------------------------------------------------------------------------------
#Get Url 
#Store the URL of current HTML that is being parsed into a variable to return later 
url = 'https://ucr.edu'

#------------------------------------------------------------------------------------------    
#Print in specified format
print()
print()
print()
print('{' + '\n')
print(' ' + '"' + 'web_title' + '"' + ' = ' + web_title)
print()
print(' ' + '"' + 'web_url' + '"' + ' = ' + url)
print()
print(' ' + '"' + 'body' + '"' + ' = ' + body)
print()
print('}' + '\n')
#------------------------------------------------------------------------------------------    





#------------------------------------------------------------------------------------------    
    
        


        
#Questions:
    #How is my data being passed to me. 
        #Will it be a folder containing HTML files or will it be a file containing html links

 
    
#htmlParse()   