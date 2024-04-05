# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 04:27:43 2021

@author: Kar
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.action_chains import ActionChains

from bs4 import BeautifulSoup
import time
import xlsxwriter


def StoringInOneExcel(results, resultFilePath):
    m = max(len(l) for l in results)
    results = [l + ['']*(m-len(l)) for l in results]
    wb = xlsxwriter.Workbook(resultFilePath)
    sheet = wb.add_worksheet()  
    
    wb = xlsxwriter.Workbook(resultFilePath)
    sheet = wb.add_worksheet()

    for row in range(len(results)):
        for col in range(len(results[0])):
            sheet.write(row, col, results[row][col])

    
    wb.close()
    
    
def setting(): #login 함수 - 로그인 까지의 정보 다룸
    global driver #다른 함수에서도 driver 변수를 활용
     
    #selenium 크롬 드라이버에서 headless 옵션 설정
    options = webdriver.ChromeOptions() 
    '''options.add_argument('headless')'''
    options.add_argument('window-size=1920x1080')
    options.add_argument("--start-maximized")
    options.add_argument("disable-gpu")
    
    #크롬 드라이버 선택 후,  headless 선택에 따라 옵션 적용 유무 선택
    #크롬 드라이버는 오픈 소스로 공개된 크롬 드라이버를 사용함 ("크롬 셀레니움 드라이버" 구글링 자료)
    
    #driver = webdriver.Chrome(wd+"\\chromedriver.exe")
    
    driver = webdriver.Chrome("chromedriver.exe", chrome_options=options)
    driver.implicitly_wait(3)

q_list = ["일산","고봉","덕양","고양","행주"]

setting()
master = [["검색어","종류","제목","저자","발행기관","발행지","일자","권수","페이지","kci 등"]]

for q in q_list:
    driver.get("https://www.dbpia.co.kr/search/topSearch?startCount=0&collection=ALL&range=A&searchField=ALL&sort=RANK&query="+q+"&srchOption=*&includeAr=false&searchOption=*")
    time.sleep(1)
    
    driver.find_elements_by_xpath("//div[@class='dropdown']")[1].click()
    time.sleep(0.3)
    driver.find_element_by_xpath("//div[@class='dropdown open']/div/div[@id='100']").click()
    time.sleep(5)
    
    temp = []
    
    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')
    pg_num = 1
    
    while True:
        
        article_list = soup.find('div',{'class':'listBody schResult'}).find('ul', {'id' : 'dev_search_list'}).find_all('li', {'class':'item'})
        for a in article_list:
            title = a.find('h5').text
            
            try:
                types = a.find('div',{'class':'typeWrap'}).find('li',{'class':'data'}).text
            except AttributeError:
                types = ""
                
            try:
                author = a.find('ul',{'class':'info'}).find('li',{'class':'author'}).text
            except AttributeError:
                author = ""
                
            try:
                publisher = a.find('ul',{'class':'info'}).find('li',{'class':'publisher'}).text
            except AttributeError:
                publisher = ""
            
            try:
                journal = a.find('ul',{'class':'info'}).find('li',{'class':'journal'}).text
            except AttributeError:
                journal = ""

            try:
                volume = a.find('ul',{'class':'info'}).find('li',{'class':'volume'}).text
            except AttributeError:
                volume = ""
                
            try:
                date = a.find('ul',{'class':'info'}).find('li',{'class':'date'}).text
            except AttributeError:
                date = ""
        
                
            try:
                page = a.find('ul',{'class':'info'}).find('li',{'class':'page'}).text
            except AttributeError:
                page = ""
                
            try:
                kci = a.find('ul',{'class':'info'}).find('li',{'class':'kci'}).text
            except AttributeError:
                kci = ""
            temp.append([q,types,title,author,publisher,journal,date,volume,page,kci])
        
        pg_num += 1
        time.sleep(2)
        try:
            if divmod(pg_num,10)[1] == 1:
                driver.find_element_by_xpath("//div[@class='paging']/a[@id='next']").click()
            else:
                driver.find_element_by_xpath("//div[@class='paging']/a[@id='pcPaging"+str(pg_num)+"']").click()
        except NoSuchElementException:
            break
        time.sleep(5)
        req = driver.page_source
        soup = BeautifulSoup(req, 'html.parser')
        
    master += temp

StoringInOneExcel(master, "result.xlsx")