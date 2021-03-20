import requests
from bs4 import BeautifulSoup
import pandas as pd
#from selenium import webdriver
#import time

#driver = webdriver.Chrome("chromedriver")

indeed_LIMIT = 50
indeed_URL = f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?q=python&limit={indeed_LIMIT}"

saramin_LIMIT = 100
saramin_URL = f"http://www.saramin.co.kr/zf_user/search/recruit?searchType=search&searchword=%ED%8C%8C%EC%9D%B4%EC%8D%AC&recruitPageCount={saramin_LIMIT}"

def extract_pages(URL):
    #driver.get(URL)
    results = requests.get(URL)
    soup = BeautifulSoup(results.text, "html.parser")
    pagination = soup.find("div", {"class": "pagination"})
    links = pagination.find_all('a')
    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))
    max_page = pages[-1]
    return max_page

def extract_indeed(html):
    title = html.find("h2", {"class": "title"}).find("a")["title"]zz
    company = html.find("span", {"class": "company"})
    company_anchor = company.find("a")
    if company_anchor is not None:
        company = company_anchor.string
    else:
        company = company.string
    company = company.strip()
    location = html.find("div", {"class": "recJobLoc"})["data-rc-loc"]
    job_id = html["data-jk"]
    return {'SITE':'INDEED','Job': title, 'Company': company, "Location": location, "Link": f"https://kr.indeed.com/viewjob?jk={job_id}"}

def extract_saramin(html):
    title = html.find("h2", {"class": "job_tit"}).find("a")["title"]
    company = html.find("div", {"class": "area_corp"})
    if company:
        company_anchor = company.find("a")
        if company_anchor is not None:
            company = company_anchor.string
        else:
            company = company.string
        company = company.strip()
    else:
        company = None
    location = html.find("div", {"class": "job_condition"}).find_all("a")
    loc = ""
    for place in location:
        loc += place.text + " "
    job_id = html["value"]
    return {'SITE':'SARAMIN','Job': title, 'Company': company, "Location": loc, "Link": f"http://www.saramin.co.kr/zf_user/jobs/relay/view?isMypage=no&rec_idx={job_id}"}

def indeed_jobs(last_page):
    jobs = pd.DataFrame()
    print('Start Scrapping from "INDEED"')
    for page in range(last_page):
        print(f"Scrapping page {page+1}")
        result = requests.get(f"{indeed_URL}&start={page*indeed_LIMIT}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
        for result in results:
            job = extract_indeed(result)
            df = pd.DataFrame.from_dict([job])
            jobs = jobs.append(df)
            #print(jobs)
    return jobs

def saramin_jobs(last_page):
    jobs = pd.DataFrame()
    print('Start Scrapping from "SARAMIN"')
    for page in range(last_page):
        print(f"Scrapping page {page+1}")
        result = requests.get(f"{saramin_URL}&start={page*saramin_LIMIT}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "item_recruit"})
        for result in results:
            job = extract_saramin(result)
            df = pd.DataFrame.from_dict([job])
            jobs = jobs.append(df)
            #print(jobs)
    return jobs


def give_me_job(URL1, URL2):

    #INDEED
    last_page_1 = extract_pages(URL1)
    #print("INDEED Last Page:",last_page_1)
    indeed = indeed_jobs(last_page_1)
    print('\n')
    #SARAMIN
    last_page_2 = extract_pages(URL2)
    print("SARAMIN Last Page:",last_page_2)
    saramin = saramin_jobs(last_page_2)

    My_Job = pd.concat([indeed,saramin])
    return My_Job.to_excel('./Jobs(Python).xlsx')

#Trial
give_me_job(indeed_URL, saramin_URL)

#print(extract_pages(saramin_URL))