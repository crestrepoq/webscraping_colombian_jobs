import requests
from bs4 import BeautifulSoup
import re
from re import search
import numpy as np
import pandas as pd
import json
import math

import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

enlace = 'https://www.linkedin.com/jobs/search/?f_TPR=r86400&geoId=100876405&location=Colombia&sortBy=DD&position=1&pageNum=0'

def parser_url(url):
    '''
    Obtener url y parsearla
    '''
    url = requests.get(url)
    soup = BeautifulSoup(url.content, 'html.parser')
    split_html = list(soup.children)
    return split_html[1]

def num_jobs(url):
    parser_link = parser_url(url)
    num_jobs = parser_link.find(class_="results-context-header__new-jobs").text
    print(num_jobs)
    num_jobs_clean = int(re.sub(r'\(|\)| new|,', '', num_jobs))
    print(num_jobs_clean)
    return num_jobs_clean

num_vacancies = num_jobs(enlace) # numero de vacantes que proporciona la pagina

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(executable_path=r'C:/Users/Cristian Restrepo/Documents/Anaconda/pkgs/python-3.7.6-h60c2a47_2/chromedriver.exe',options=options)
driver.get(enlace)

ScrollNumber = math.ceil(num_vacancies/25) # 25 es un estimado de cantidad de vacantes promedio por scroll
for i in range(1,ScrollNumber):
    try:
        element = driver.find_element_by_xpath('/html/body/div[1]/div/main/section/button')
        driver.execute_script("arguments[0].click();", element)
        time.sleep(10)
        driver.execute_script("window.scrollTo(1,50000)")
        time.sleep(5)
    except:
        driver.execute_script("window.scrollTo(1,50000)")
        time.sleep(5)

file = open('prueba.html', 'w')
file.write(driver.page_source)
file.close()

driver.close()

url = open('prueba.html','r')

# print(url)
