# -*- coding: utf-8 -*-
"""
Created on Wed May  2 21:55:14 2018

@author: Andy Cheung
"""

#%%
"""
List of industries and their symbols:

Financials - Banks: 5011
Financials - Insurance: 5021
Financials - Investments & Assets Management: 5031
Financials - Other Financials: 5032
Financials - Securities: 5041
"""

#%%
"""Import pkg"""
import pandas as pd
import time
from selenium import webdriver

#%%
"""Open browser"""
my_path = r"C:\Users\user\Desktop\chromedriver"
browser = webdriver.Chrome(executable_path = my_path)
browser.maximize_window()

"""Websites to be scraped"""
url_form = "http://www.aastocks.com/en/stocks/market/industry/sector-industry-details.aspx?industrysymbol={}&t={}&hk=0" #URL form
industry_sym = "5011" #Enter your industry symbol here
datafile = r"C:\data_{}_summary.csv" #Enter your path for data file here
summaryfile = r"C:\data_{}.csv" #Enter your path for summary file here

#%%
def get_element(xpath):
     target_list = []
     text = browser.find_elements_by_xpath(xpath)
     for i in range(len(text)):
         target_list.append(text[i].text)
         
     return target_list

def get_content(df, get_list, company_list, count):
    for i in range(1, len(company_list)+1):
        data = []
        for j in get_list:
            data_xpath = "//tbody//tr[{}]//td[{}]"
            data.append(get_element(data_xpath.format(str(i), str(j)))[-1])
        if count == 0:
            df.iloc[i-1, :] = [company_list[i-1]] + data
        else:
            df.iloc[i-1, :] = data

    return df

#%%
"""Getting a list of companies"""
browser.get(url_form.format(industry_sym, 1))
time.sleep(3)
browser.execute_script("window.scrollTo(0, 3000)")

company_name_and_code_xpath = "//tbody//tr//td[1]//div[1]//div//span[1]"
company_list = get_element(company_name_and_code_xpath)

"""Scraping data and save it into a dataframe"""
page = ["1", "2", "4", "6"]
sleep_sec = 3
index_list = range(len(company_list))
extr_col_array = [["company", "current price", "change in price", "percentage change in price", "volume", "turnover", "PE", "PB", "yield", "market cap"],
                  ["one-month", "two-month", "three-month", "fiftytwo-week"],
                  ["current ratio", "quick ratio", "roa", "roe", "gp margin", "np margin", "payout", "DE"],
                  ["revenue", "EPS", "revenue growth", "EPS growth"]]
[df1, df2, df3, df4] = [pd.DataFrame(index=index_list, columns=extr_col_array[0]), pd.DataFrame(index=index_list, columns=extr_col_array[1]),pd.DataFrame(index=index_list, columns=extr_col_array[2]),pd.DataFrame(index=index_list, columns=extr_col_array[3])] 
df = [df1, df2, df3, df4]
get_list_array = [range(3, 12), range(4, 8), range(4, 12), [4, 10, 5, 11]]
count = 0

for index in page:
    browser.get(url_form.format(industry_sym, index))
    time.sleep(sleep_sec)
    browser.execute_script("window.scrollTo(0, 3000)")
    df[count] = get_content(df[count], get_list_array[count], company_list, count)
    count = count + 1
     
#%%
df = pd.concat([df1, df2, df3, df4], axis = 1)
print(df)

"""Summary statistics & convert char to numeric """
remove_sym_list = [",", "%", "N/A"]
format_col_lbl = ["volume", "turnover", "market cap", "revenue"]
replace_unit_array = [[".", ""], ["K", "000"], ["M", "000000"],["B", "000000000"]]
head_end_list = [range(1, 10), range(14, 25)]
for remove_sym in remove_sym_list:
    df = df.applymap(lambda x: str(x.replace(remove_sym, "")))
    
for replace_unit_list in replace_unit_array:
    df[format_col_lbl] = df[format_col_lbl].applymap(lambda x: str(x.replace(replace_unit_list[0], replace_unit_list[1])))

for num in head_end_list:
    for i in num:
        df.iloc[:, i] = pd.to_numeric(df.iloc[:, i])

print(df.describe())
df.describe().to_csv(datafile.format(industry_sym), sep = ",", index = True)
df.to_csv(summaryfile.format(industry_sym), sep = ",", index = False)

browser.quit()
