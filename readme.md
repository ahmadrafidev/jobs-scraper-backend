# Jobs Scraper Backend

Repository ini adalah bagian backend untuk proyek Jobs Scraper yang dibangun menggunakan FastAPI dan MongoDB untuk menyediakan layanan API yang mengakses data lowongan pekerjaan dari beberapa situs web terkemuka di Indonesia.

## Teknologi yang Digunakan

- **Bahasa Pemrograman:**
  - Python: Digunakan untuk pengembangan job scraper dan API server.
  - JavaScript/TypeScript: Digunakan untuk mengembangkan aplikasi klien (web dan mobile).
- **Framework Backend:**
  - FastAPI: Framework untuk membangun API backend yang cepat dan mudah digunakan.
- **Database:**
  - MongoDB: Database NoSQL untuk menyimpan data lowongan pekerjaan yang dikumpulkan oleh scraper.
- **Client-side Technologies:**
  - **Web client framework:** NextJS 
  - **Mobile client framework:** React Native (Expo)
- **Hosting/Deployment:**
  - Vercel, GCP, atau AWS: Platform untuk hosting aplikasi dan API, dipilih berdasarkan kemudahan deployment, keandalan, dan fitur.

## API Endpoints

API Server memberikan layanan-layanan berikut:

1. **Informasi Lowongan dari Semua Jenis Pekerjaan:**
   - Endpoint: `GET /jobs`
   - Mengambil semua data lowongan pekerjaan dari MongoDB.

2. **Informasi Lowongan Berdasarkan Filter:**
   - Endpoint: `GET /jobs/search`
   - Mengambil data lowongan pekerjaan berdasarkan filter seperti `title`, `company`, `location`, `start_date`, dan `end_date`.
   - Contoh query:
     - `/jobs/search?title=Programmer`
     - `/jobs/search?company=IBM`
     - `/jobs/search?location=Jakarta`
     - `/jobs/search?start_date=2023-01-01&end_date=2023-12-31`

3. **Informasi Lowongan Berdasarkan ID:**
   - Endpoint: `GET /jobs/{job_id}`
   - Mengambil data lowongan pekerjaan berdasarkan `job_id`.

## Instalasi dan Menjalankan Aplikasi

1. **Clone Repository:**
   ```sh
   git clone https://github.com/ahmadrafidev/jobs-scraper-backend.git
   cd jobs-scraper-backend
   ```

2. Instalasi Dependensi
  ```
  pipenv install
  pipenv shell
  pip install fastapi uvicorn pymongo pydantic
  ```

3. Menjalankan Aplikasi 
  ```
  uvicorn main:app --reload --host 0.0.0.0 --port 8000
  ```

4. Mengakses API
   1. Buka browser atau mengakses tools seperti `curl` atau `Postman` untuk mengakses endpoint:
      1. http://localhost:8000/jobs
      2. http://localhost:8000/jobs/{job_id}
      3. http://localhost:8000/jobs/search?title=Programmer

