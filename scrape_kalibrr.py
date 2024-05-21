import asyncio
from pyppeteer import launch
import json

urls = [
    'https://www.kalibrr.com/home/te/programmer',
    'https://www.kalibrr.com/home/te/network',
    'https://www.kalibrr.com/home/te/data',
    'https://www.kalibrr.com/home/te/cyber-security'
]

async def scrape_job_listings(url):
    browser = await launch()
    page = await browser.newPage()
    await page.goto(url)

    await asyncio.sleep(5)

    await page.waitForSelector('.k-container.k-grid', timeout=60000)

    jobs = await page.evaluate('''() => {
        const jobElements = document.querySelectorAll('.k-container.k-grid .k-font-dm-sans.k-rounded-lg.k-bg-white.k-border-solid.k-border');
        let jobList = [];
        jobElements.forEach(job => {
            let title = job.querySelector('h2 a') ? job.querySelector('h2 a').innerText : '';
            let company = job.querySelector('span.k-inline-flex.k-items-center.k-mb-1 a') ? job.querySelector('span.k-inline-flex.k-items-center.k-mb-1 a').innerText : '';
            let location = job.querySelector('.k-flex.k-gap-4.k-text-gray-300 span.k-text-gray-500.k-block') ? job.querySelector('.k-flex.k-gap-4.k-text-gray-300 span.k-text-gray-500.k-block').innerText : '';
            let salary = job.querySelector('.k-flex.k-gap-4.k-text-gray-300 p.k-text-gray-500') ? job.querySelector('.k-flex.k-gap-4.k-text-gray-300 p.k-text-gray-500').innerText : 'Salary Undisclosed';
            let type = job.querySelector('.k-flex.k-gap-4.k-items-center.k-text-gray-300 span.k-text-gray-500') ? job.querySelector('.k-flex.k-gap-4.k-items-center.k-text-gray-300 span.k-text-gray-500').innerText : '';
            jobList.push({title, company, location, salary, type});
        });
        return jobList;
    }''')

    await browser.close()
    return jobs

async def scrape_all_jobs(urls):
    all_jobs = []
    for url in urls:
        jobs = await scrape_job_listings(url)
        all_jobs.extend(jobs)
    return all_jobs

if __name__ == "__main__":
    jobs = asyncio.run(scrape_all_jobs(urls))

    # Simpan hasil scraping ke file JSON
    with open('jobs_kalibrr.json', 'w', encoding='utf-8') as f:
        json.dump(jobs, f, ensure_ascii=False, indent=4)
