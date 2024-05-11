from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

# Setup MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['job_scraper']
collection = db['jobs']

# Define the FastAPI app
app = FastAPI()

# Pydantic models for request and response bodies
class Job(BaseModel):
    id: Optional[str]
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

@app.get("/jobs", response_model=List[Job])
def get_jobs():
    jobs = list(collection.find())
    if not jobs:
        raise HTTPException(status_code=404, detail="No jobs found")
    return jobs

@app.get("/jobs/{job_id}", response_model=Job)
def get_job(job_id: str):
    job = collection.find_one({"_id": ObjectId(job_id)})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@app.get("/jobs/search", response_model=List[Job])
def search_jobs(
    title: Optional[str] = None,
    company: Optional[str] = None,
    location: Optional[str] = None,
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
    return jobs

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
