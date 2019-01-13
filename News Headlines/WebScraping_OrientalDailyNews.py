# -*- coding: utf-8 -*-
"""
Created on Fri Sep  7 09:19:46 2018

@author: user
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
#%%
Today = '20180908' #Input date here in yyyymmdd format
OrientalDaily = 'http://orientaldaily.on.cc/cnt/news/{}/index.html'
FilePath = r'C:\Users\user\Documents\Database\Oritental Daily News' #Change the path here
FileName = r'\OrientalDailyHeadLine' + Today + '.csv'

#%%
OrientalDaily = OrientalDaily.format(Today)

def FindHeader(TextList):
    MinLen = 4
    HeaderList = list(filter(lambda x: len(x) > MinLen, TextList))
    return HeaderList

def WebScrapeData(OrientalDaily):
    UrlSource = requests.get(OrientalDaily)
    UrlPrettified = BeautifulSoup(UrlSource.content, 'html.parser', from_encoding='utf-8')
    
    DataTables = UrlPrettified.find_all('li', {'class':''})
    DataList = FindHeader([i.text for i in DataTables])
    return DataList
    #Check encoding before BeautifulSoup is applied by UrlSource.encoding 
    #Check encoding after applying BeautifulSoup by UrlPrettified.original_encoding
    #Type meta in serach html of the webpage to check for charset

def DataCleaning():
    DfHeader = pd.DataFrame(WebScrapeData(OrientalDaily), columns=[Today])
    DfHeader.to_csv(FilePath+FileName, sep=',', index=False, encoding='utf_8_sig')
    
DataCleaning()
