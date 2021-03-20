import requests
from bs4 import BeautifulSoup
import datetime
#from selenium import webdriver

t = datetime.datetime.now()
y = t.year
m = t.month
d = t.day
date = str(y)+'-'+str(m)+'-'+str(d)

def extract_pages(url):
  results = requests.get(url)
  soup = BeautifulSoup(results.text, "html.parser")
  pagination = soup.find("div", {"class": "pagination"})
  links = pagination.find_all('a')
  pages = []
  for link in links[:-1]:
    pages.append(int(link.string))
  max_page = pages[-1]
  return max_page

def extract_indeed(html):
  title = html.find("h2", {"class": "title"}).find("a")["title"]
  company = html.find("span", {"class": "company"})
  if company is not None:
    company_anchor = company.find("a")
    if company_anchor is not None:
      company = company_anchor.string
    else:
      company = company.string
  else:
      company = company
  location = html.find("div", {"class": "recJobLoc"})["data-rc-loc"]
  job_id = html["data-jk"]
  return {'Job': title, 'Company': company, "Location": location, "Link": f"https://kr.indeed.com/viewjob?jk={job_id}"}

def extract_saramin(html):
  title = html.find("h2", {"class": "job_tit"}).find("a")["title"]
  company = html.find("div", {"class": "area_corp"})
  if company is not None:
    company_anchor = company.find("a")
    if company_anchor is not None:
      company = company_anchor.string
    else:
      company = company.string
  else:
      company = company
  loc = html.find("div", {"class": "job_condition"}).find_all("a")
  location = ""
  for place in loc:
      location += place.text + " "
  job_id = html["value"]
  return {'Job': title, 'Company': company, "Location": location, "Link": f"http://www.saramin.co.kr/zf_user/jobs/relay/view?isMypage=no&rec_idx={job_id}"}
    
def indeed_jobs(last_page,url):
  jobs = []
  print('Start Scrapping from "INDEED"')
  for page in range(last_page):
    print(f"Scrapping page {page+1}")
    result = requests.get(f"{url}&start={page*50}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
    for result in results:
      job = extract_indeed(result)
      jobs.append(job)
  return jobs

def saramin_jobs(last_page, url):
    jobs = []
    print('Start Scrapping from "SARAMIN"')
    for page in range(last_page):
        print(f"Scrapping page {page+1}")
        result = requests.get(f"{url}&start={page*100}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "item_recruit"})
        for result in results:
            job = extract_saramin(result)
            jobs.append(job)
    return jobs

def give_me_job(keyword):
  # indeed_LIMIT = 50
  indeed_URL = f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?q={keyword}&limit=50"
  saramin_URL = f"http://www.saramin.co.kr/zf_user/search/recruit?searchType=search&searchword={keyword}&recruitPageCount=100"
  last_page_1 = extract_pages(indeed_URL)
  last_page_2 = extract_pages(saramin_URL)
  jobs = indeed_jobs(last_page_1, indeed_URL)
  jobs2 = saramin_jobs(last_page_2, saramin_URL)
  jobs.append(jobs2)
  return jobs