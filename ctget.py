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
from selenium.common.exceptions import NoSuchElementException


#
#"C:\1\selenium\chromedriver\111\chromedriver.exe"
class contentget: 
    def __init__(self,url=''):  
        selepath=r'C:/Users/ws199/.cache/selenium/chromedriver/win32/114.0.5735.90/chromedriver.exe'
        self.seleniumpath=selepath
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_experimental_option('w3c', False)
        self.driver = webdriver.Chrome(self.seleniumpath, options=chrome_options)
        print(url)
        self.driver.get(url)
        time.sleep(5)

    def go_to_next_page(self,xpath):
        # x='/html/body/div[1]/div/main/div[1]/div/article/div[3]/div/ul/li[5]/a/'
        # next_page_button=WebDriverWait(self.driver, 7).until(lambda x: x.find_element(By.XPATH,xpath))
        # self.driver.execute_script('arguments[0].click();', next_page_button)
        try:
            next_page_button = self.driver.find_element_by_xpath("/html/body/div[1]/div/main/div[1]/div/article/div[3]/div/ul/li[5]/a/text()")
            #next_page_button = self.driver.find_element_by_css_selector("a.sc-iuhXDa.dBEucF") #下一页按钮的class名
            self.driver.execute_script("arguments[0].click();", next_page_button)
            time.sleep(3)
            return True
        except NoSuchElementException:
            print("已经到达最后一页")
            return False

     
    
    def run(self):
        #x='/html/body/div[1]/div/main/div[1]/div/article'
        while True:
            x='/html/body/div[1]/div/main/div[1]/div/article/div[1]'
            try:
                x=self.driver.find_element(By.XPATH,x).text
                
                #print(x) #新闻内容     
                return x
            except:
                print('网络不通或者不是当前可用网址')
            if not self.go_to_next_page():
                break    

# x=contentget(url='https://news.yahoo.co.jp/articles/03a7a4170efa9257b3960136aa451d0237b82aaa')
# x.run()
