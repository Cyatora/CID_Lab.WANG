import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import requests
from urllib.parse import urlparse
import urllib.parse
import json
import os
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from ctget import *
import sqlite3
from doc2vec2 import v2cv
import threading

def sqlconnect():
    dird=os.path.dirname(os.path.abspath(__file__))
    dbpath=os.path.join(dird,"text.db")
    return sqlite3.connect(dbpath)

def insertdb_(name,comment,url,times,content):
    match=v2cv(comment,content)
    args=(name,comment,url,times,str(match[0]))   #####
    conn=sqlconnect()
    c=conn.cursor()
    dd='insert into info (name,comment,url,times,vecmatch) values(?,?,?,?,?)'  #####
    c.execute(dd,args)
    
    conn.commit()

class commentget: 
    def __init__(self,selepath=r'C:/Users/ws199/.cache/selenium/chromedriver/win32/114.0.5735.90/chromedriver.exe',url='',url1=''): 
        
        self.seleniumpath=selepath
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')  
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36')
        chrome_options.add_experimental_option('w3c', False)
        self.url=url
        self.url1=url1
        self.driver = webdriver.Chrome(self.seleniumpath, options=chrome_options)
        
        self.content=contentget(url=self.url1).run()
        print('Start')
        self.driver.get(url)
        
    def checkurl(self):
        headers={
            'Accept-CH': 'Sec-CH-UA-Full-Version-List, Sec-CH-UA-Model, Sec-CH-UA-Platform-Version, Sec-CH-UA-Arch',
            'Age': '0',
            'Cache-Control': 'private, no-cache, no-store, must-revalidate',
            'Connection': 'keep-alive',
            'Content-Encoding': 'gzip',
            'Content-Type': 'text/html;charset=UTF-8',
            'Date': 'Thu, 09 Mar 2023 06:52:19 GMT',
            'Permissions-Policy': 'ch-ua-full-version-list=*, ch-ua-model=*, ch-ua-platform-version=*, ch-ua-arch=*',

            'Strict-Transport-Security': 'max-age=15552000'}
        r=requests.get(self.url,headers=headers)
        #print(r.status_code)
        return r.status_code
    def buttom_click_xpath(self,xpath):
        profilelink=WebDriverWait(self.driver, 7).until(lambda x: x.find_element(By.XPATH,xpath))
        self.driver.execute_script('arguments[0].click();', profilelink)
    def buttom_click_selector(self,css):
        profilelink=WebDriverWait(self.driver, 7).until(lambda x: x.find_element(By.XPATH,css))
        self.driver.execute_script('arguments[0].click();', profilelink)
    def input(self,obj,key): 
        obj.send_keys(key)    
    
    def run(self):
        st=self.checkurl()
        if st==200:
            try:
                time.sleep(7)
                url=self.driver.current_url
                y=self.driver.page_source
                file=open('1.html','w',encoding='utf-8')
                file.write(y)
                file.close()
                
                dird=os.path.dirname(os.path.abspath(__file__))
                dird=dird.replace('\\','/')
                self.driver.get(f'file://{dird}/1.html')

                x='/html/body/div[1]/div/main/div[1]/div[1]/article'

                time.sleep(3)
                u=self.driver.find_element_by_xpath(x)
                u=u.get_attribute('innerHTML')
                
                file=open('1.html','w',encoding='utf-8')
                file.write(u)
                file.close()
                
                self.run2(url)
                

            except Exception as e:
                print('Error:',e)
                pass
        else:
            print('末页')
            return False
        
    def run2(self,url):
        dird=os.path.dirname(os.path.abspath(__file__))
        dird=dird.replace('\\','/')
        self.driver.get(f'file://{dird}/1.html')
        x=self.driver.find_elements_by_xpath('/html/body/div[2]/ul[2]/li')
        #print(x)
        
        for i in x:
            name=i.find_element_by_css_selector('h2').text
            comment=i.find_element_by_css_selector('.UserCommentItem__Comment-eoheEU.cTIZmn').text
            times=i.find_element_by_css_selector('time').text
            print('============',times,name,comment,'============')
            insertdb_(name,comment,url,times,self.content)
        return True