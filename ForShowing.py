import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import time

t = datetime.datetime.now()
y = t.year
m = t.month
d = t.day
date = str(y)+'-'+str(m)+'-'+str(d)

keyword = input("Enter the keyword: ").capitalize()

indeed_LIMIT = 50
indeed_URL = f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?q={keyword}&limit={indeed_LIMIT}"

saramin_LIMIT = 100
saramin_URL = f"http://www.saramin.co.kr/zf_user/search/recruit?searchType=search&searchword={keyword}&recruitPageCount={saramin_LIMIT}"


def extract_pages(URL):
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
    title = html.find("h2", {"class": "title"}).find("a")["title"]
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
    return {'SITE':'SARAMIN', 'Job': title, 'Company': company,"Location": loc, "Link": f"http://www.saramin.co.kr/zf_user/jobs/relay/view?isMypage=no&rec_idx={job_id}"}

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
    return jobs

def returnJobs():

    global indeed_URL
    global saramin_URL
    global keyword
    global date

    print("\n<<Start Extracting>>")
    print("-"*200)
    
    #INDEED
    last_page_1 = extract_pages(indeed_URL)
    print(f"INDEED Total Pages: {last_page_1}\n")
    indeed = indeed_jobs(last_page_1)
    print("-"*200)

    #SARAMIN
    last_page_2 = extract_pages(saramin_URL)
    print(f"SARAMIN Total Pages: {last_page_2}\n")
    saramin = saramin_jobs(last_page_2)
    print("-"*200)

    print("<<Extracting is Done!>>\n")
    jobFile = pd.concat([indeed, saramin])
    new_index = [i for i in range(1,len(jobFile))]
    jobFile= jobFile.reset_index(drop=True).reindex(new_index)
    print(jobFile)
    return jobFile

def saveJobs(job):

    global keyword
    global date
    
    print('Do you want to save?: [ y / n ]')
    key = input().lower()

    filename = f'[{date}]Jobs({keyword}).xlsx'

    if key == 'y':
        job.to_excel(filename)
        print("Save Done.\n")
        print("Do you want me to send this file to your email?: [y/n]")
        sendKey = input().lower()
        if sendKey == 'y':
            sendJobs(filename)
        else:
            print("Sending operation quited.\n")
    else:
        print("Save operation quited.\n")

def sendJobs(attachment):
    #Sender Info
    me = 'bugbugoasis2021@gmail.com' # you must change here as your email
    my_password = 'bugbugoasis2021' # Your password

    # Login
    s = smtplib.SMTP_SSL('smtp.gmail.com')
    s.login(me, my_password)

    # Reciever Info
    email_list = []
    while 1:
        email = input("Enter your Email Addresses(stop: -1): ")
        if email != '-1':
            email_list.append(email)
        else:
            break
    
    for you in email_list:
        # Email Info
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"{attachment} from. BugBug"
        msg['From'] = me
        msg['To'] = you

        # Email Contents
        content = f"Here is your Job informations. Have a great day!"
        part2 = MIMEText(content, 'plain')
        msg.attach(part2)

        part = MIMEBase('application', "octet-stream")
        with open(f"./{attachment}", 'rb') as file:
            part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment", filename=f"{attachment}")
            msg.attach(part)

        # Sending Email and quit server
        s.sendmail(me, you, msg.as_string())
        print("\nSending", end="")
        for i in range(1,4):
            print('.'*i, end='\b'*i)
            time.sleep(1)
        print("\nEmail is sented!")

    s.quit()

# Run
jobs = returnJobs()
saveJobs(jobs)