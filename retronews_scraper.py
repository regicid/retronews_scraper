from selenium.webdriver.firefox.options import Options
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
import multiprocessing as mtp
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep
import re
import os
from defs import browser


def retronews_scraper(url): #L'URL peut soit être une URL retronews, soit une URL gallica redirigeant vers retronews
    options = Options()
    options.headless = True
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.cache.disk.enable", False)
    profile.set_preference("browser.cache.memory.enable", False)
    profile.set_preference("browser.cache.offline.enable", False)
    profile.set_preference("network.http.use-cache", False)
    driver = webdriver.Firefox(options=options)
    #driver = webdriver.Firefox(profile,options=options)
    driver.get(url)
    sleep(3)
    webElem = driver.find_element(By.CSS_SELECTOR,".css-1wuy641")
    webElem.click()
    webElem = driver.find_element(By.CSS_SELECTOR,".ocr")
    webElem.click()
    sleep(2)
    if driver.current_url.find("gallica")>0 or driver.current_url == "https://www.retronews.fr/":
        print("error"+driver.current_url)
        return ""
    soup = BeautifulSoup(driver.page_source)
    if soup.find("div",{"class":"side-panel"}).text == '' or soup.find("div",{"class":"block-header"}) is None:
        print("error"+driver.current_url)
        return ""
    soup = BeautifulSoup(driver.page_source)
    nb_pages = soup.find("div",{"class":"block-header page"})
    nb_pages = int(nb_pages.text.replace("\n","").split("/")[-1])
    url = driver.current_url 
    url = re.sub(".$","",url)
    Text = str()
    for i in range(nb_pages):
        url2 = url+str(i+1)
        driver.get(url2)
        sleep(2)
        soup = BeautifulSoup(driver.page_source)
        text = soup.find("div",{"class":"block-body page"})
        if text is not None:
            text = text.text
            Text += " \n " + text
            print(i)
    return Text
