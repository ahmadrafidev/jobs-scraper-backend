from fastapi import FastAPI, BackgroundTasks, HTTPException, Query
from pymongo import MongoClient
from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId
from scraper.scraper import scrape_jobstreet, scrape_karir, scrape_kalibrr, scrape_linkedin, keywords_urls

# Setup MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['job_scraper']
collection = db['jobs']

# Define the FastAPI app
app = FastAPI()

# Pydantic models for request and response bodies
class Job(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    title: Optional[str]
    company: Optional[str]
    location: Optional[str]
    date_posted: Optional[datetime]
    source: Optional[str]
    job_link: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat()
        }

# Keywords to search for
keywords = ["programmer", "data", "network", "cyber security"]

@app.get("/jobs", response_model=List[Job])
def get_jobs():
    jobs = list(collection.find())
    if not jobs:
        raise HTTPException(status_code=404, detail="No jobs found")
    
    # Convert MongoDB ObjectId to string and rename _id to id
    for job in jobs:
        job["_id"] = str(job["_id"])
    
    return jobs

@app.get("/jobs/{job_id}", response_model=Job)
def get_job(job_id: str):
    try:
        job = collection.find_one({"_id": ObjectId(job_id)})
    except:
        raise HTTPException(status_code=404, detail="Invalid job ID")
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job["_id"] = str(job["_id"])
    return job

@app.get("/jobs/search", response_model=List[Job])
def search_jobs(
    title: Optional[str] = Query(None, min_length=1),
    company: Optional[str] = Query(None, min_length=1),
    location: Optional[str] = Query(None, min_length=1),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    query = {}
    if title:
        query['title'] = {'$regex': title, '$options': 'i'}
    if company:
        query['company'] = {'$regex': company, '$options': 'i'}
    if location:
        query['location'] = {'$regex': location, '$options': 'i'}
    if start_date and end_date:
        query['date_posted'] = {'$gte': start_date, '$lte': end_date}
    elif start_date:
        query['date_posted'] = {'$gte': start_date}
    elif end_date:
        query['date_posted'] = {'$lte': end_date}

    jobs = list(collection.find(query))
    if not jobs:
        raise HTTPException(status_code=404, detail="No jobs match the search criteria")
    
    # Convert MongoDB ObjectId to string and rename _id to id
    for job in jobs:
        job["_id"] = str(job["_id"])
    
    return jobs

@app.post("/scrape")
def trigger_scrape(background_tasks: BackgroundTasks):
    for keyword, url in keywords_urls.items():
        background_tasks.add_task(scrape_jobstreet, url, keyword)
        background_tasks.add_task(scrape_karir, keyword)
        background_tasks.add_task(scrape_kalibrr, keyword)
    return {"message": "Scraping tasks have been initiated"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
