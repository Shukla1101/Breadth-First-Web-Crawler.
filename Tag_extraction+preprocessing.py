# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import csv
import nltk
import pandas as pd
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from nltk import PorterStemmer
import requests
from bs4 import BeautifulSoup
from IntegratedCleaningAndStop import stem ,stopword ,nonASCII, remove_alphanumeric

def function(s):
    final_str=nonASCII(s)
    final_str=remove_alphanumeric(final_str)
    final_str=stopword(final_str)
    final_str=stem(final_str)
    final_str.lower()
    return final_str
to_remove=["yandex","yahoo","ask","duckduckGo","aol","bing","terms of use","privacy policy","curlie","curlie"
           "facebook","twitter","linkedin","google","ecosia","gigablast","startpage","about","become an editor",
           "suggest a site","help","forums","login","donate"]

list_URLs = [""]
final_list =[]
count=0;
while count<2000 and len(list_URLs)!=0:
    temp_list=[]
    URL = list_URLs.pop(0)
    count=count+1
    r = requests.get(URL) 
    soup = BeautifulSoup(r.content, 'html.parser')
    temp_list.append(URL)
   
        
    
    title= " "
    if soup.title is not None:
        title = soup.title.string
    temp_list.append(function(title))
    
    meta_desc = " "
    keywords =  " "
    for meta in soup.find_all('meta'):
        if meta.get('name') == 'description' and meta.get('content') is not None :
            meta_desc = meta_desc + meta.get('content')
        
        if meta.get('name') == 'keywords' and meta.get('content') is not None:
            keywords = keywords + meta.get('content')
    temp_list.append(function(meta_desc))
    temp_list.append(function(keywords))
       
    h1_str = " "
    for h1 in soup.find_all('h1'):
        if h1.string is not None:
            h1_str = h1_str + h1.string +" "
    temp_list.append(function(h1_str))  
    
    h2_str = " "
    for h2 in soup.find_all('h2'):
        if h2.string is not None:
            h2_str = h2_str + h2.string +" "
    temp_list.append(function(h2_str))  
    
    h3_str = " "
    for h3 in soup.find_all('h3'):
        if h3.string is not None:
            h3_str = h3_str + h3.string +" "
    temp_list.append(function(h3_str))
    
    
    a_str = " "
    for link in soup.find_all('a'):
        if link.string is not None and link.string.lower() not in to_remove :
            a_str = a_str + link.string +" "
        if link.get('href') is not None and 'http' in  link.get('href') and link.get('href') not in list_URLs and link.string is not None and link.string.lower() not in to_remove:
            list_URLs.append(link.get('href'))
    temp_list.append(function(a_str))   
        
    p_str = " "
    for ptags in soup.find_all('p'):
        if ptags.string is not None:
           p_str = p_str + ptags.string +" "
    temp_list.append(function(p_str))
  
    s_str = " "
    for stags in soup.find_all('strong'):
        if stags.string is not None:
            s_str = s_str + stags.string +" "
    temp_list.append(function(s_str))

    b_str = " "
    for btags in soup.find_all('b'):
        if btags.string is not None:
            b_str = b_str + btags.string +" "
    temp_list.append(function(b_str)) 

    list_str = " "
    for list_tags in soup.find_all('li'):
        if list_tags.string is not None:
            list_str = list_str + list_tags.string +" "
    temp_list.append(function(list_str))
    
    i_str = " "
    for itags in soup.find_all('i'):
        if itags.string is not None:
            i_str = i_str + itags.string +" "
    temp_list.append(function(i_str))
    
    em_str = " "
    for emtags in soup.find_all('em'):
        if emtags.string is not None:
            em_str = em_str + emtags.string +" "
    temp_list.append(function(em_str))
    
    with open("Final_sheet.csv", "a") as fp:
        wr = csv.writer(fp, dialect='excel')
        wr.writerow(temp_list)
    ##final_list.append(temp_list)

##df = pd.DataFrame(final_list, columns =['URL', 'Title','MetaDescription', 'Keywords','H1', 'H2','H3', 'AnchorText','Paragraph', 'Strong','Bold', 'List_str','Italic', 'Emphasis'])
##df.to_csv('Final_sheet.csv')



