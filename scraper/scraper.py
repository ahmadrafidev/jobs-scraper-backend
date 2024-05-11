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

if __name__ == "__main__":
    scrape_jobstreet()
