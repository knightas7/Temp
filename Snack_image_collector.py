# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 10:36:18 2021

@author: Kar
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.action_chains import ActionChains

import urllib

global driver

from bs4 import BeautifulSoup


def setting(): #login 함수 - 로그인 까지의 정보 다룸
    global driver #다른 함수에서도 driver 변수를 활용
     
    #selenium 크롬 드라이버에서 headless 옵션 설정
    options = webdriver.ChromeOptions() 
    '''options.add_argument('headless')'''
    options.add_argument('window-size=1920x1080')
    options.add_argument("--start-maximized")
    options.add_argument("disable-gpu")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    
    #크롬 드라이버 선택 후,  headless 선택에 따라 옵션 적용 유무 선택
    #크롬 드라이버는 오픈 소스로 공개된 크롬 드라이버를 사용함 ("크롬 셀레니움 드라이버" 구글링 자료)
    
    #driver = webdriver.Chrome(wd+"\\chromedriver.exe")
    
    driver = webdriver.Chrome("chromedriver.exe", chrome_options=options)
    driver.implicitly_wait(3)
    driver.get("https://brightside.me/")
    
def check_url():
    url = driver.current_url
    if url[:21] == "https://brightside.me":
        #crawl_brightside()
        crawl_brightside_soup()

def crawl_brightside():
    global num
    input("다운로드 할 포스팅에서 엔터키를 눌러주세요.")
    image_list = driver.find_elements_by_xpath("//div[@tabindex='-1']/div[contains(@data-test-id,'article-image')]")
    print(len(image_list))
    for img in image_list:
        num += 1
        print(num)
        image = img.find_element_by_xpath(".//img")
        src = image.get_attribute('src')
        
        if src[-4] == '.':
            last = src[-4:]
        elif src[-5] == '.':
            last = src[-5:]
        else:
            raise "확장자에러"
        urllib.request.urlretrieve(src, "C:\\Users\\Kar\\Desktop\\downloaded_image\\image"+str(num)+last)

def crawl_brightside_soup():
    global driver
    category_num = 0
    while True:
        category_num += 1
        num = 0
        input("다운로드 할 포스팅에서 엔터키를 눌러주세요.")
        req = driver.page_source
        soup = BeautifulSoup(req, 'html.parser')
        
        image_list = soup.find_all("div",{'tabindex' : '-1'})
        print(str(len(image_list)) + "개 사진 다운로드를 시작합니다~")
        for img in image_list:
            num += 1
            image = img.find('div',attrs={'data-test-id': lambda e: e.startswith('article-image') if e else False})
            image2 = image.find('img')
            src = image2['src']
            if src[-4] == '.':
                last = src[-4:]
            elif src[-5] == '.':
                last = src[-5:]
            else:
                raise "확장자에러"
            urllib.request.urlretrieve(src, "downloaded_image\\image"+str(category_num)+"_"+str(num)+last)
#crawl_brightside_soup()
setting()
check_url()