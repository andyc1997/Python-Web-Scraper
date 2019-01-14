# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 21:29:52 2019

@author: AndyC
"""
#Put the package to the folder
import sys
sys.path.append(r'C:\Users\user\Documents\Note on Python\Air Quality')
from epdAirpkg import epdAir

#Example
epdAir.getHist('SHATIN', ['Carbon Monoxide', 'Ozone'], 'daily', '2005/6/2', '2005/7/2')
print(epdAir.getAQHI('2018', '01'))
print(epdAir.plotMap('all'))