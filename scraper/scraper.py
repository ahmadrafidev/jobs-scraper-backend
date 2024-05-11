import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['job_scraper']
collection = db['jobs']

# Function to scrape job listings from jobstreet.co.id
def scrape_jobstreet():
    url = "https://www.jobstreet.co.id/en/job-search/job-vacancy.php?ojs=10&key=programmer"  # URL to scrape
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
            'scrape_date': datetime.now()
        }

        collection.update_one({'job_link': job_link}, {'$set': job_data}, upsert=True)
        print(f"Inserted/Updated job: {title} at {company}")

# Function to scrape job listings from karir.com
def scrape_karir():
    url = "https://www.karir.com/search/jobs?keywords=programmer"  # URL to scrape
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
            'scrape_date': datetime.now()
        }

        collection.update_one({'job_link': job_link}, {'$set': job_data}, upsert=True)
        print(f"Inserted/Updated job: {title} at {company}")

# Function to scrape job listings from kalibrr.com
def scrape_kalibrr():
    url = "https://www.kalibrr.com/job-board/te/job-openings?keywords=programmer"  # URL to scrape
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
            'scrape_date': datetime.now()
        }

        collection.update_one({'job_link': job_link}, {'$set': job_data}, upsert=True)
        print(f"Inserted/Updated job: {title} at {company}")

# Function to scrape job listings from linkedin.com
def scrape_linkedin():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    url = "https://www.linkedin.com/jobs/search?keywords=programmer"  # URL to scrape
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
            'scrape_date': datetime.now()
        }

        collection.update_one({'job_link': job_link}, {'$set': job_data}, upsert=True)
        print(f"Inserted/Updated job: {title} at {company}")

if __name__ == "__main__":
    scrape_jobstreet()
    scrape_karir()
    scrape_kalibrr()
    scrape_linkedin()
