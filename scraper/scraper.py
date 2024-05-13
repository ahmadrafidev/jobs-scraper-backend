import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['job_scraper']
collection = db['jobs']

# Keywords to search for
keywords = ["programmer", "data", "network", "cyber security"]

def scrape_jobstreet(keyword):
    url = f"https://www.jobstreet.co.id/en/job-search/job-vacancy.php?ojs=10&key={keyword}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    jobs = soup.find_all('div', class_='sx2jih0 zcydq8e sx2jih7 zcydq84o zcydq83n zcydq8t zcydq810 zcydq84v zcydq84p zcydq81l')

    for job in jobs:
        title = job.find('div', class_='sx2jih0 zcydq8p').text.strip() if job.find('div', class_='sx2jih0 zcydq8p') else None
        company = job.find('span', class_='sx2jih0 zcydq84u zcydq842 zcydq852 zcydq86 zcydq84p').text.strip() if job.find('span', class_='sx2jih0 zcydq84u zcydq842 zcydq852 zcydq86 zcydq84p') else None
        location = job.find('span', class_='sx2jih0 zcydq84u zcydq852').text.strip() if job.find('span', class_='sx2jih0 zcydq84u zcydq852') else None
        date_posted = job.find('time')['datetime'] if job.find('time') else None
        job_link = job.find('a')['href'] if job.find('a') else None
        
        # Insert into MongoDB
        job_data = {
            'title': title,
            'company': company,
            'location': location,
            'date_posted': date_posted,
            'source': 'jobstreet.co.id',
            'job_link': job_link,
            'scrape_date': datetime.now(),
            'keyword': keyword
        }

        collection.update_one({'job_link': job_link}, {'$set': job_data}, upsert=True)
        print(f"Inserted/Updated job: {title} at {company} for keyword: {keyword}")

def scrape_karir(keyword):
    url = f"https://karir.com/search-lowongan?keyword={keyword}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    jobs = soup.find_all('div', class_='job-card')

    for job in jobs:
        title = job.find('h4', class_='job-title').text.strip() if job.find('h4', class_='job-title') else None
        company = job.find('div', class_='company-name').text.strip() if job.find('div', class_='company-name') else None
        location = job.find('div', class_='job-location').text.strip() if job.find('div', class_='job-location') else None
        date_posted = job.find('span', class_='posted-date').text.strip() if job.find('span', class_='posted-date') else None
        job_link = job.find('a')['href'] if job.find('a') else None
        
        # Insert into MongoDB
        job_data = {
            'title': title,
            'company': company,
            'location': location,
            'date_posted': date_posted,
            'source': 'karir.com',
            'job_link': job_link,
            'scrape_date': datetime.now(),
            'keyword': keyword
        }

        collection.update_one({'job_link': job_link}, {'$set': job_data}, upsert=True)
        print(f"Inserted/Updated job: {title} at {company} for keyword: {keyword}")

def scrape_kalibrr(keyword):
    url = f"https://www.kalibrr.com/job-board/te/job-openings?keywords={keyword}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    jobs = soup.find_all('div', class_='k-grid-container')

    for job in jobs:
        title = job.find('h3', class_='k-card-title').text.strip() if job.find('h3', class_='k-card-title') else None
        company = job.find('span', class_='k-text-subdued').text.strip() if job.find('span', class_='k-text-subdued') else None
        location = job.find('span', class_='k-job-location').text.strip() if job.find('span', class_='k-job-location') else None
        date_posted = job.find('span', class_='k-job-postdate').text.strip() if job.find('span', class_='k-job-postdate') else None
        job_link = job.find('a')['href'] if job.find('a') else None
        
        # Insert into MongoDB
        job_data = {
            'title': title,
            'company': company,
            'location': location,
            'date_posted': date_posted,
            'source': 'kalibrr.com',
            'job_link': job_link,
            'scrape_date': datetime.now(),
            'keyword': keyword
        }

        collection.update_one({'job_link': job_link}, {'$set': job_data}, upsert=True)
        print(f"Inserted/Updated job: {title} at {company} for keyword: {keyword}")

def scrape_linkedin(keyword):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    url = f"https://www.linkedin.com/jobs/search?keywords={keyword}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    jobs = soup.find_all('div', class_='result-card__contents')

    for job in jobs:
        title = job.find('h3', class_='result-card__title').text.strip() if job.find('h3', class_='result-card__title') else None
        company = job.find('h4', class_='result-card__subtitle').text.strip() if job.find('h4', class_='result-card__subtitle') else None
        location = job.find('span', class_='job-result-card__location').text.strip() if job.find('span', class_='job-result-card__location') else None
        date_posted = job.find('time')['datetime'] if job.find('time') else None
        job_link = job.find('a')['href'] if job.find('a') else None
        
        # Insert into MongoDB
        job_data = {
            'title': title,
            'company': company,
            'location': location,
            'date_posted': date_posted,
            'source': 'linkedin.com',
            'job_link': job_link,
            'scrape_date': datetime.now(),
            'keyword': keyword
        }

        collection.update_one({'job_link': job_link}, {'$set': job_data}, upsert=True)
        print(f"Inserted/Updated job: {title} at {company} for keyword: {keyword}")

if __name__ == "__main__":
    for keyword in keywords:
        scrape_jobstreet(keyword)
        scrape_karir(keyword)
        scrape_kalibrr(keyword)
        scrape_linkedin(keyword)
