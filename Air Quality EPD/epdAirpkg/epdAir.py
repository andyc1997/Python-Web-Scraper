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
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select

#Get real time data for all districts
def __checkLocation(location):
    csvFile = os.path.dirname(__file__)
    csvPath = os.path.join(csvFile, 'statid.csv')
    statId = pd.read_csv(csvPath)
    return statId[statId.station == location].iloc[0, 1:3]

def __cleanData(text):
    airTable = text.find('td', {'class':'H24C_ColDateTime'})
    airData = []
    for i in range(0, 7):
        if i == 0:
            airData.append(airTable.text.replace('\xa0', ' '))
        else:
            airTable = airTable.next_sibling
            airData.append(pd.to_numeric(airTable.text.replace('-', ''), 'coerce'))
    return airData
    
def __getLocation(location):
    statId = __checkLocation(location)
    airURL = 'http://www.aqhi.gov.hk/en/aqhi/past-24-hours-pollutant-concentration{}.html?stationid={}'
    airGetWeb = requests.get(airURL.format(statId[1], statId[0]))
    airUrlP = BeautifulSoup(airGetWeb.content, 'html.parser', from_encoding='utf-8')
    return __cleanData(airUrlP)

def __normalize(data):
    return data/np.nanmedian(data)*100

def plotMap(indicator):
    csvFile = os.path.dirname(__file__)
    csvPath = os.path.join(csvFile, 'statid.csv')
    statId = pd.read_csv(csvPath)
    n = statId.shape[0]
    arrId = []
    statColumn = ['Date', 'NO2', 'O3', 'SO2', 'CO', 'PM10', 'PM2.5']
    for location in statId.station:
        arrId.append(__getLocation(location))
    airTable = statId.join(pd.DataFrame(arrId, columns=statColumn))
    
    if indicator != 'all':
        pyplot.scatter(airTable.E, airTable.N, marker='o', c=airTable[indicator], s=__normalize(airTable[indicator]), cmap='Greens', edgecolors='black')
        for i in range(0, n):
            pyplot.text(airTable.E[i]+0.01, airTable.N[i]-0.01, airTable['station'][i])
        pyplot.title(indicator + ' in Hong Kong' + airTable.Date[0])
        pyplot.show()
        
    elif indicator == 'all':
        pyplot.figure(figsize=(20, 10))
        index = 1
        statColumn.remove('Date')
        for indicator in statColumn:
            pyplot.subplot(2, 3, index)
            pyplot.scatter(airTable.E, airTable.N, marker='o', c=airTable[indicator], s=__normalize(airTable[indicator]), cmap='Greens', edgecolors='black')
            for i in range(0, n):
                pyplot.text(airTable.E[i]+0.01, airTable.N[i]-0.01, airTable['station'][i])
            pyplot.title(indicator + ' in Hong Kong ' + airTable.Date[0])
            index = index + 1
        pyplot.show()
    return airTable
#%%
#Read data file of AQHI from EPD to pandas dataframe directly
def __reqAQHI(year, month):
    urlAQHI = 'http://www.aqhi.gov.hk/epd/ddata/html/history/{}/{}{}_Eng.csv'
    row_to_be_skipped = 7
    return pd.read_csv(urlAQHI.format(year, year, month), sep=",", delimiter=",", 
                       skiprows=row_to_be_skipped)

def getAQHI(year, month):
    dfAQHI = __reqAQHI(year, month).fillna(method='ffill')
    return dfAQHI[dfAQHI.Hour != 'Daily Max']
#%%
#Past Data 
"""
Reference:
    location: 
        CENTRAL/WESTERN
        EASTERN
        KWAI CHUNG
        KWUN TONG
        SHAM SHUI PO
        SHATIN
        TAI PO
        TAP MUN
        TSEUNG KWAN O
        TSUEN WAN
        TUEN MUN
        TUNG CHUNG
        YUEN LONG
        Roadside Stations
        CAUSEWAY BAY
        CENTRAL
        MONG KOK
    para: Carbon Monoxide, Fine Suspended Particulates, Nitrogen Dioxide, Nitrogen Oxides, 
        Ozone,  Respirable Suspended Particulates, Sulphur Dioxide
    timerng: hourly, daily, monthly, yearly
    from_date: format yyyy/m/d e.g. 1997/6/3
    to_date: format yyyy/m/d e.g. 1997/6/3
"""
def getHist(location, para, timerng, from_date, to_date):
    airURL = 'https://cd.epic.epd.gov.hk/EPICDI/air/station/?lang=en'
    driverFile = os.path.dirname(__file__)
    webdriver_path = os.path.join(driverFile,'chromedriver')
    browser = webdriver.Chrome(executable_path = webdriver_path)
    browser.get(airURL)
    time.sleep(2)
    
    __getDist(location.upper(), browser)
    __getPara(para, browser)
    __getTimeRng(timerng, browser)
    __submit(browser)
    if timerng == 'hourly':
        limit = 366
        if __checkDate(from_date, to_date) <= limit:
            __getTimePrd(timerng, 'From', from_date, browser)
            __getTimePrd(timerng, 'To', to_date, browser)
    elif timerng == 'daily':
        limit = 31
        if __checkDate(from_date, to_date) <= limit:
            __getTimePrd(timerng, 'From', from_date, browser)
            __getTimePrd(timerng, 'To', to_date, browser)           
    elif timerng == 'monthly':
        limit = 60
        if __checkDate(from_date, to_date)/31.0 <= limit: #Approximately
            __getTimePrd(timerng, 'From', from_date, browser)
            __getTimePrd(timerng, 'To', to_date, browser)        
    elif timerng == 'yearly':
        __getTimePrd(timerng, 'From', from_date, browser)
        __getTimePrd(timerng, 'To', to_date, browser)     
    __submit(browser)
    time.sleep(2)
    browser.quit()

def __getDist(location, browser): 
    airDist = browser.find_element_by_link_text(location)
    airDist.click()

def __getPara(para, browser):
    for i in para:
        checkbox = browser.find_element_by_xpath("//*[text()='" + i + "']")
        checkbox.click()

def __getTimeRng(timerng, browser): #hourly, daily, monthly, yearly
    text = timerng
    checkbox = browser.find_element_by_xpath("//input[@value='" + text + "']")
    checkbox.click()

def __getDate(date): #yyyy/m/d
    return date.split('/')

def __checkDate(from_date, to_date):
    diffDate = abs(pd.to_datetime(from_date) - pd.to_datetime(to_date))
    return diffDate.days
    
def __selectTimePrd(date, select):
    for i in select.options:
        if i.text == date:
            i.click()

def __getTimePrd(timerng, way ,date, browser):
    if timerng == 'hourly' or timerng == 'daily':
        listDate = ['Year', 'Month', 'Day']
        for (date, d) in zip(__getDate(date), listDate):
            text = way + d
            select = Select(browser.find_element_by_xpath("//select[@id='form:daily" + text + "']"))
            __selectTimePrd(date, select)        
    elif timerng == 'monthly':
        listDate = ['Year', 'Month']
        for (date, d) in zip(__getDate(date)[0:2], listDate):
            text = way + d
            select = Select(browser.find_element_by_xpath("//select[@id='form:monthly" + text + "']"))
            __selectTimePrd(date, select)
    elif timerng == 'yearly':
        d = 'Year'
        date = __getDate(date)[0]
        text = way + d
        select = Select(browser.find_element_by_xpath("//select[@id='form:yearly" + text + "']"))
        __selectTimePrd(date, select)
        
def __submit(browser):
    submit = browser.find_element_by_xpath("//*[text()='Download CSV']")
    submit.click()