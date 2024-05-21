import asyncio
from pyppeteer import launch
import json

urls = [
    'https://www.jobstreet.co.id/id/data-jobs',
    'https://www.jobstreet.co.id/id/network-jobs',
    'https://www.jobstreet.co.id/id/cyber-security-jobs',
    'https://www.jobstreet.co.id/id/programmer-jobs'
]

async def scrape_job_listings(url):
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.goto(url)

    await asyncio.sleep(5)

    await page.waitForSelector('#app > div > div:nth-child(7) > div > section > div:nth-child(2) > div > div > div > div > div > div.y735df0._1iz8dgsr._1iz8dgsp._1iz8dgsgy._1aon4mx0._1aon4mx8 > div > div > div.y735df0._21bfxf1 > div > div:nth-child(2)', timeout=60000)

    jobs = await page.evaluate('''() => {
        const jobElements = document.querySelectorAll('#app > div > div:nth-child(7) > div > section > div:nth-child(2) > div > div > div > div > div > div.y735df0._1iz8dgsr._1iz8dgsp._1iz8dgsgy._1aon4mx0._1aon4mx8 > div > div > div.y735df0._21bfxf1 > div > div:nth-child(2)');
        let jobList = [];
        jobElements.forEach(job => {
            let title = job.querySelector('h1 a') ? job.querySelector('h1 a').innerText : '';
            let company = job.querySelector('span[data-automation="company-name"]') ? job.querySelector('span[data-automation="company-name"]').innerText : '';
            let location = job.querySelector('span[data-automation="job-location"]') ? job.querySelector('span[data-automation="job-location"]').innerText : '';
            jobList.push({title, company, location});
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
    with open('jobs_jobstreet.json', 'w', encoding='utf-8') as f:
        json.dump(jobs, f, ensure_ascii=False, indent=4)