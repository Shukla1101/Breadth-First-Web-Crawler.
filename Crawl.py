import csv
import requests
from bs4 import BeautifulSoup
from IntegratedCleaningAndStop import stem ,stopword ,nonASCII, remove_alphanumeric,prep
from requests.exceptions import ConnectionError
from singlepagecrawler import crawl
import nltk
import pandas as pd
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from nltk import PorterStemmer
##Functions used
def write_to_csv(temp_list):
    with open("Final_sheet.csv", "a") as fp:
        wr = csv.writer(fp, dialect='excel')
        wr.writerow(temp_list)
###########
        
head=['URL', 'Title','MetaDescription', 'Keywords','H1', 'H2','H3', 'AnchorText','Paragraph', 'Strong','Bold', 'List_str','Italic', 'Emphasis']
write_to_csv(head)
count=0
curlie_link=["https://curlie.org/en/Business/#"]
sites=[]

while count<2500 and len(curlie_link)!=0:
    URL=curlie_link.pop(0)
    
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    
    try:
        page = requests.get(URL, headers=headers, timeout=10)
        page.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",URL)
        continue
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",URL)
        continue
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",URL)
        continue
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else",URL)
        continue
    
    
    if page.status_code!=200:
        continue
    
    soup = BeautifulSoup(page.content, 'html.parser')
    
    for div_curlie in soup.find_all('div',class_="cat-item"):
        if div_curlie.a.get('href') not in curlie_link:
            curlie_link.append("https://curlie.org"+div_curlie.a.get('href'))
    
    
    for div in soup.find_all('div',class_="title-and-desc"):
        if div.a.get('href') not in sites:
            sites.append(div.a.get('href'))
            write_to_csv(crawl(div.a.get('href'),prep(div.get_text(separator=','))))
            count=count+1
            print("Site Crawled=",div.a.get('href'),"count =",count,"\n")
            

         



    

        
        
  