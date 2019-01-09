# -*- coding: utf-8 -*-
"""
Created on Sat Sep  8 21:32:16 2018

@author: user
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
#%%
Today = '20180911'
FilePath = r'C:\Users\user\Documents\Database\Apple Daily News'
FileName = r'\AppleDailyHeadLine' + Today + '.csv'

#%%
AppleDaily = 'https://hk.appledaily.com/archive/index/' + Today + '/index/'

def DataCleaning(OldDataList, RemoveText):
    NewDataList = list(map(lambda x: x.replace(RemoveText, '') , OldDataList))
    return NewDataList

def WebScrapeData(AppleDaily):
    UrlSource = requests.get(AppleDaily)
    UrlPrettified = BeautifulSoup(UrlSource.content, 'html.parser', from_encoding='utf-8')
    ParentTables = UrlPrettified.find('div', {'class':'ArchiveContainerLHS'})
    ChildrenTables = ParentTables.findChildren('li')
    
    DataList = [Datum.text for Datum in ChildrenTables]
    for RemoveText in ['\n', '\u3000']:
        DataList = DataCleaning(DataList, RemoveText)
    return DataList

def CreateDataFile():
    DfHeader = pd.DataFrame(WebScrapeData(AppleDaily), columns=[Today])
    DfHeader.to_csv(FilePath+FileName, sep=',', index=False, encoding='utf_8_sig')
    
#%%
CreateDataFile()
