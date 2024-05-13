# Jobs Scraper Backend

This repository is the backend for the Jobs Scraper project which was built using FastAPI and MongoDB to provide API services that access job vacancy data from several leading websites in Indonesia.

## Technology Used

- **Programming language:**
   - Python: Used for job scraper and API server development.
   - JavaScript/TypeScript: Used to develop client applications (web and mobile).
- **Backend Framework:**
   - FastAPI: A framework for building fast and easy-to-use backend APIs.
- **Database:**
   - MongoDB: NoSQL database for storing job vacancy data collected by the scraper.
- **Client-side Technologies:**
   - **Web client framework:** NextJS
   - **Mobile client framework:** React Native (Expo)
- **Hosting/Deployment:**
   - Vercel, GCP, or AWS: Platforms for hosting applications and APIs, selected based on ease of deployment, reliability, and features.

## API Endpoints

API Server provides the following services:

1. **Vacancy Information for All Types of Jobs:**
   - Endpoint: `GET /jobs`
   - Retrieves all job vacancy data from MongoDB.

2. **Vacancy Information Based on Filter:**
 - Endpoint: `GET /jobs/search`
 - Retrieve job vacancy data based on filters such as `title`, `company`, `location`, `start_date`, and `end_date`.
 - Example query:
   - `/jobs/search?title=Programmer`
   - `/jobs/search?company=IBM`
   - `/jobs/search?location=Jakarta`
   - `/jobs/search?start_date=2023-01-01&end_date=2023-12-31`

3. **Vacancy Information Based on ID:**
   - Endpoint: `GET /jobs/{job_id}`
   - Retrieve job vacancy data based on `job_id`.

## Installing and Running Applications

1. **Clone Repository:**
   ```sh
   git clone https://github.com/ahmadrafidev/jobs-scraper-backend.git
   cd jobs-scraper-backend
   ```

2.Dependency Installation
  ```
  pipenv install
  pipenv shell
  pip install fastapi uvicorn pymongo pydantic
  ```

3. Running the application 
  ```
  uvicorn main:app --reload --host 0.0.0.0 --port 8000
  ```

4. Accessing the API
   1. Open a browser or access a tool such as `curl` or `Postman` to access the endpoint:
      1. http://localhost:8000/jobs
      2. http://localhost:8000/jobs/{job_id}
      3. http://localhost:8000/jobs/search?title=Programmer

**Note**: 

1. The web client service that handles user interaction via the website can be accessed via the repository: [Jobs Scraper Website](https://github.com/ahmadrafidev/jobs-scraper-web)
2. Mobile client services that handle user interactions via mobile applications can be accessed through the repository: [Jobs Scraper Mobile](https://github.com/ahmadrafidev/jobs-scraper-mobile)