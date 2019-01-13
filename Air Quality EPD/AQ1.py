# -*- coding: utf-8 -*-
"""
Created on Sat Jan 12 17:09:23 2019
@Project: Air pollution: Real time Web scraper & visualization
@author: AndyC
"""
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from matplotlib import pyplot
import requests
import os
#%%    
def checkLocation(location):
    csvFile = os.getcwd()
    csvPath = os.path.join(csvFile, 'statid.csv')
    statId = pd.read_csv(csvPath)
    return statId[statId.station == location].iloc[0, 1:3]

def cleanData(text):
    airTable = text.find('td', {'class':'H24C_ColDateTime'})
    airData = []
    for i in range(0, 7):
        if i == 0:
            airData.append(airTable.text.replace('\xa0', ' '))
        else:
            airTable = airTable.next_sibling
            airData.append(pd.to_numeric(airTable.text.replace('-', ''), 'coerce'))
    return airData
    
def getLocation(location):
    statId = checkLocation(location)
    airURL = 'http://www.aqhi.gov.hk/en/aqhi/past-24-hours-pollutant-concentration{}.html?stationid={}'
    airGetWeb = requests.get(airURL.format(statId[1], statId[0]))
    airUrlP = BeautifulSoup(airGetWeb.content, 'html.parser', from_encoding='utf-8')
    return cleanData(airUrlP)

def normalize(data):
    return data/np.nanmedian(data)*100
#%%
def plotMap(indicator):
    csvFile = os.getcwd()
    csvPath = os.path.join(csvFile, 'statid.csv')
    statId = pd.read_csv(csvPath)
    n = statId.shape[0]
    arrId = []
    statColumn = ['Date', 'NO2', 'O3', 'SO2', 'CO', 'PM10', 'PM2.5']
    for location in statId.station:
        arrId.append(getLocation(location))
    airTable = statId.join(pd.DataFrame(arrId, columns=statColumn))
    
    if indicator != 'all':
        pyplot.scatter(airTable.E, airTable.N, marker='o', c=airTable[indicator], s=normalize(airTable[indicator]), cmap='Greens', edgecolors='black')
        for i in range(0, n):
            pyplot.text(airTable.E[i]+0.01, airTable.N[i]-0.01, airTable['station'][i])
        pyplot.title(indicator+' in Hong Kong' + airTable.Date[0])
        pyplot.show()
        
    elif indicator == 'all':
        pyplot.figure(figsize=(20, 10))
        index = 1
        statColumn.remove('Date')
        for indicator in statColumn:
            pyplot.subplot(2, 3, index)
            pyplot.scatter(airTable.E, airTable.N, marker='o', c=airTable[indicator], s=normalize(airTable[indicator]), cmap='Greens', edgecolors='black')
            for i in range(0, n):
                pyplot.text(airTable.E[i]+0.01, airTable.N[i]-0.01, airTable['station'][i])
            pyplot.title(indicator + ' in Hong Kong ' + airTable.Date[0])
            index = index + 1
        pyplot.show()
    return airTable
#%%
plotMap('all')
