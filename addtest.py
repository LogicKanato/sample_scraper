import pandas as pd
import numpy as np
# from selenium.webdriver.common.by import By
# from selenium import webdriver

# from re import search
# links = ['?Id=MER2021Q1-1041&Language=E&View=M&MemberId=3aa3f283-f56c-4eb9-ada7-5c1676027d36', '?Id=MER2021Q1-1041&Language=E&View=R&ReportItemId=10140']
# print(links)
# keyword = 'View=M&Member'
# result = []
# for link in links:
#     if search(keyword, link):
#         # print("hello")
#         result.append(link)
    
# print(result)
# name = 'Aboultaif,\r\n\t\t\t\t\t\t\t\t\t\tZiad'
# print(name)
# name = name.replace('\r\n\t\t\t\t\t\t\t\t\t\t','')
# print(name)

# PATH = 'C:/Users/kanat/scrape/WebDriver/chromedriver.exe'
# driver = webdriver.Chrome(PATH)
# driver.get('https://www.ourcommons.ca/PublicDisclosure/Archive/MemberExpenditures.aspx?Language=E&Year=2009-2010')

# name = 'cb_1546_Abbott, Hon. Jim_Kootenay-Columbia'
# box = driver.find_element_by_name(name)
# box.click()
# nextpage = 'ctl00$PageContent$CreateReport'
# button = driver.find_element_by_name(nextpage)
# button.click()

file_name =  '2018Q1.csv'
df = pd.read_csv(file_name)
num_data = len(df.index)
for row in range (0,num_data):
    for x in df.columns:
        print(df.loc[row,x], type(df.loc[row,x]))
