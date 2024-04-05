# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 19:16:23 2024

@author: knigh
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import smtplib
from email.mime.text import MIMEText


def settings():
    global driver, last_list
    
    driver = webdriver.Chrome()
    driver.get('https://www.g2b.go.kr/index.jsp')

    close_popup()
    
    time.sleep(3)
    
    driver.switch_to.frame("maintop_iframe")
    search_input = driver.find_element(By.XPATH,"//input[@id='AKCKwd']")
    search_input.send_keys("만족도\n")
    time.sleep(5)
    close_popup()
    
    driver.switch_to.frame("sub")
    
    result_list = driver.find_elements(By.XPATH,"//ul[@class='search_list']/li/strong/a")
    
    last_list = []
    for l in last_list:
        last_list.append([l.text])


def get_more_info(new_list):
    global driver
    
    


def send_email(title, context):
    try:
        smtp = smtplib.SMTP('smtp.gmail.com', 587)     
        smtp.set_debuglevel(True)
        sender = 'alarmbot4896'
        reciever = 'taxi@k-edutech.com'
        password = 'urphynlibrfcxftw'
        smtp.starttls()
        smtp.login(sender,password)
        
        msg = MIMEText(title+'\n'+context+'\n\n자동 발송된 메일입니다.')
        msg['Subject'] = title
        msg['From'] = sender
        msg['To'] = reciever
        
        smtp.sendmail(sender, reciever, msg.as_string())
            
    except Exception as e:
        print('error', e)
    
    finally:
        if smtp is not None:
            smtp.quit()
    

def close_popup():
    global driver
    popup_list = driver.window_handles
    
    for p in popup_list:
        if p != popup_list[0]:
            driver.switch_to.window(p)
            driver.close()
            driver.switch_to.window(popup_list[0])

def searching():
    global driver
    driver.switch_to.default_content()
    driver.switch_to.frame("tops")
    search_input = driver.find_element(By.XPATH,"//input[@id='AKCKwd']")
    search_input.send_keys("만족도\n")
    time.sleep(5)
    close_popup()


def fetching_comparing():
    global driver, last_list, new_list
    
    driver.switch_to.default_content()
    driver.switch_to.frame("sub")
    result_list = driver.find_elements(By.XPATH,"//ul[@class='search_list']/li/strong/a")
    
    new_list = []
    fetch_list = []
    for r in result_list:
        new_list.append([r.text,r])
    
    for l in new_list:
        if l[0] not in last_list:
            fetch_list.append(l[0])

    print(fetch_list)
    for f in fetch_list:
        time.sleep(1)
        print(f)
        driver.switch_to.default_content()
        driver.switch_to.frame("sub")
        result_list = driver.find_elements(By.XPATH,"//ul[@class='search_list']/li/strong/a")
        
        
        for r in result_list:
            if f == r.text:
                r.click()
                time.sleep(3)
                driver.switch_to.frame("bodyFrame")
                title = driver.find_elements(By.XPATH,"//table[@summary='공고일반 정보']/tbody/tr")[2].text
                title = title.replace("\n"," : ")

                client = driver.find_elements(By.XPATH,"//table[@summary='공고일반 정보']/tbody/tr")[3].text
                client = client.replace("\n"," : ")
                
                send_email(title,client)
                
                time.sleep(1)
                driver.back()
                time.sleep(3)
                break
            


    last_list = []
    for l in new_list:
        last_list.append(l[0])


        

if __name__ == "__main__":
    settings()


searching()
fetching_comparing()
