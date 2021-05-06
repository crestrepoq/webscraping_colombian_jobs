import requests
from bs4 import BeautifulSoup
import re
from re import search
import numpy as np
import pandas as pd
import json

url = 'https://www.linkedin.com/jobs/search/?f_TPR=r604800&geoId=100876405&location=Colombia&sortBy=DD'

def parser_url(url):
    url = requests.get(url)
    soup = BeautifulSoup(url.content, 'html.parser')
    split_html = list(soup.children)
    return split_html[1]

#Obtener la lista de urls correspondientes a cada trabajo en una pagina
def url_jobs(url_parser):
    urls_jobs = list()
    for link in url_parser.find_all(class_="result-card__full-card-link"):
    #for link in jobs.find_all(class_="result-card__full-card-link"):
        link_job = link.get('href')
        urls_jobs.append(link_job)
    return urls_jobs

def get_urls_jobs(url):
    list_urls = list()
    count = 0
    times = 0
    while times <= 5:
        url_search = url + '&start=' + str(count)
        list_urls.append(url_search)
        count = count + 25
        times = times + 1

    return list_urls


def list_urls_jobs(list_urls_searchs):
    jobs_urls = list()
    for i in range(len(list_urls_searchs)):
        link_parser = parser_url(list_urls_searchs[i])
        links_jobs = url_jobs(link_parser)
        for i in range(len(links_jobs)):
            jobs_urls.append(links_jobs[i])
    
    return jobs_urls

jobs = get_urls_jobs(url)
jobs_urls = list_urls_jobs(jobs)

print(jobs_urls)