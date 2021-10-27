from bs4 import BeautifulSoup
from requests_html import HTMLSession
from selenium.webdriver.common.by import By
from selenium import webdriver
from re import search
import pandas as pd

links = [
    "https://www.ourcommons.ca/PublicDisclosure/MemberExpenditures.aspx?Id=MER2021Q1-1041&Language=E",
    "https://www.ourcommons.ca/PublicDisclosure/MemberExpenditures.aspx?Id=MER2020Q2-1023&Language=E",
    "https://www.ourcommons.ca/PublicDisclosure/MemberExpenditures.aspx?Id=MER2020Q1-1019&Language=E",
    "https://www.ourcommons.ca/PublicDisclosure/MemberExpenditures.aspx?Id=MER2020Q3-1035&Language=E",
    "https://www.ourcommons.ca/PublicDisclosure/MemberExpenditures.aspx?Id=MER2020Q4-1037&Language=E",
    "https://www.ourcommons.ca/PublicDisclosure/MemberExpenditures.aspx?Id=MER2019Q1&Language=E",
    "https://www.ourcommons.ca/PublicDisclosure/MemberExpenditures.aspx?Id=MER2019Q2&Language=E",
    "https://www.ourcommons.ca/PublicDisclosure/MemberExpenditures.aspx?Id=MER2019Q3-A&Language=E",
    "https://www.ourcommons.ca/PublicDisclosure/MemberExpenditures.aspx?Id=MER2019Q4&Language=E",
    "https://www.ourcommons.ca/PublicDisclosure/MemberExpenditures.aspx?Id=MER2018Q1&Language=E",
    "https://www.ourcommons.ca/PublicDisclosure/MemberExpenditures.aspx?Id=MER2018Q2&Language=E",
    "https://www.ourcommons.ca/PublicDisclosure/MemberExpenditures.aspx?Id=MER2018Q3&Language=E",
    "https://www.ourcommons.ca/PublicDisclosure/MemberExpenditures.aspx?Id=MER2018Q4&Language=E",
    "https://www.ourcommons.ca/PublicDisclosure/MemberExpenditures.aspx?Id=MER2017Q5&Language=E",
    "https://www.ourcommons.ca/PublicDisclosure/MemberExpenditures.aspx?Id=MER2017Q2D&Language=E",
    "https://www.ourcommons.ca/PublicDisclosure/MemberExpenditures.aspx?Id=MER2017Q3B&Language=E",
    "https://www.ourcommons.ca/PublicDisclosure/MemberExpenditures.aspx?Id=MER2017Q4B&Language=E",
    "https://www.ourcommons.ca/PublicDisclosure/MemberExpenditures.aspx?Id=MER2016Q1&Language=E",
    "https://www.ourcommons.ca/PublicDisclosure/MemberExpenditures.aspx?Id=MER2016Q2&Language=E",
    "https://www.ourcommons.ca/PublicDisclosure/MemberExpenditures.aspx?Id=MER2016Q3&Language=E",
    "https://www.ourcommons.ca/PublicDisclosure/MemberExpenditures.aspx?Id=MER2016Q4&Language=E",
    "https://www.ourcommons.ca/PublicDisclosure/MemberExpenditures.aspx?Id=MER2015Q1&Language=E",
    "https://www.ourcommons.ca/PublicDisclosure/MemberExpenditures.aspx?Id=MER2015Q2V1&Language=E",
    "https://www.ourcommons.ca/PublicDisclosure/MemberExpenditures.aspx?Id=MER2015Q3&Language=E",
    "https://www.ourcommons.ca/PublicDisclosure/MemberExpenditures.aspx?Id=MER2015FY&Language=E",
    "https://www.ourcommons.ca/PublicDisclosure/MemberExpenditures.aspx?Id=MER2014FY&Language=E",
    "https://www.ourcommons.ca/PublicDisclosure/MemberExpenditures.aspx?Id=MER2013FY&Language=E",
  ]

old_links = [
  "https://www.ourcommons.ca/PublicDisclosure/MemberExpenditures.aspx?Language=E&Year=2011-2012",
  "https://www.ourcommons.ca/PublicDisclosure/MemberExpenditures.aspx?Language=E&Year=2010-2011",
  "https://www.ourcommons.ca/PublicDisclosure/MemberExpenditures.aspx?Language=E&Year=2009-2010"
]

s = HTMLSession()
All_pages = [] ## All expenditure pages. All_page[i] = list of all expenditure pages for i th link in the list 'links'

def getdata(url):
  r = s.get(url)
  soup = BeautifulSoup(r.text, 'html.parser')
  return soup

def getpages(soup):
  keyword = 'View=M&Member'
  result = []
  for link in soup.find_all('a'):
    if search(keyword,str(link.get('href'))):
      result.append('https://www.ourcommons.ca/PublicDisclosure/MemberExpenditures.aspx' + link.get('href'))
  return result
  

def get_report(url,result_list):

  result = {}  
  count = 0

  soup = getdata(url)

  table_header = soup.find_all('tr', {'class' : 'mer-style-member'})
  rows = table_header[count].find_all('td')
  
  result['Name'] = rows[0].text.strip().replace('\r\n\t\t\t\t\t\t\t\t\t\t','')
  result['Status'] = rows[1].text.strip()
  result['Constituency name'] = rows[2].text.strip()
  result['Constituency size'] = rows[3].text.strip().replace('\xa0','')
  result['Number of electors'] = rows[4].text.strip()


  table = soup.find_all('tr',{'class' : ['mer-style-category','mer-style-subCategory']})
  footers = soup.find_all('tr',{'class' : 'mer-style-footer'})

  for row in table:
    title = row.find('th').text.strip()
    items = row.find_all('td',{'class' : 'mer-style-value'})

    total = items[2].text.strip()
    result[title] = total

  footer_title = footers[count].find('th').text.strip()
  footer_item = footers[count].find_all('td',{'class' : 'mer-style-value'})[2].text.strip()
  result[footer_title] = footer_item
  count = count + 1

  result_list.append(result)
  # print(result)

def get_old_report(url):
  result = {}
  count = 0

  soup = getdata(url)

  # table_header = soup.find_all('tr', {'class' : 'mer-style-member'})
  # rows = table_header[count].find_all('td')
  
  # result['Name'] = rows[0].text.strip().replace('\r\n\t\t\t\t\t\t\t\t\t\t','')
  # result['Status'] = rows[1].text.strip()
  # result['Constituency name'] = rows[2].text.strip()
  # result['Constituency size'] = rows[3].text.strip().replace('\xa0','')
  # result['Number of electors'] = rows[4].text.strip()


  table = soup.find_all('tr',{'class' : ['MainCategoryRow','SubCategoryRow']})
  footers = soup.find_all('tr',{'class' : 'TotalRow'})

  for row in table:
    title = row.find('td',{'class' : ['hotspot MainCategory','hotspot SubCategory']}).text.strip()
    items = row.find_all('td')[1:]

    print(title + ' : ' + items)

  #   col = items[2].text.strip()
  #   result[title] = col

  # footer_title = footers[count].find('th').text.strip()
  # footer_item = footers[count].find_all('td',{'class' : 'mer-style-value'})[2].text.strip()
  # result[footer_title] = footer_item
  # count = count + 1
  # print(result)
 
def get_old_report_url(url):
  PATH = 'C:/Users/kanat/scrape/WebDriver/chromedriver.exe'
  driver = webdriver.Chrome(PATH)

  driver.get(url)

  name = 'cb_1546_Abbott, Hon. Jim_Kootenay-Columbia'
  box = driver.find_element_by_name(name)
  box.click()
  nextpage = 'ctl00$PageContent$CreateReport'
  button = driver.find_element_by_name(nextpage)
  button.click()
  link = driver.current_url
  return link


result = []

for link in links:
  All_pages.append(getpages(getdata(link)))

page1 = All_pages[0]
for page in page1:
  get_report(page,result)
# for pages in All_pages:
#   for page in pages:
#     get_report(page,result)

df = pd.DataFrame(result)
df.to_csv('result.csv')



# url = 'https://www.ourcommons.ca/PublicDisclosure/Archive/MemberExpenditures.aspx?Language=E&Year=2009-2010'
# print(get_old_report_url(url))
# get_old_report(url)



