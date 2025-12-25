# 🚀 Kasparro Backend Assignment

A backend service built using **FastAPI**, **PostgreSQL**, and **Docker** that ingests cryptocurrency data from multiple sources, normalizes it, and exposes REST APIs for querying and monitoring ingestion statistics.

---

## 📌 Features

* FastAPI-based REST backend
* PostgreSQL database
* Data ingestion from:

  * CoinPaprika public API
  * CSV file
* Normalized crypto asset storage
* Raw data tracking
* ETL checkpoint tracking
* Dockerized setup (API + DB)
* Swagger/OpenAPI documentation
* Health and monitoring endpoints

---

## 🛠 Tech Stack

* **Backend:** FastAPI
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy
* **Data Ingestion:** Requests, CSV
* **Containerization:** Docker & Docker Compose
* **Testing:** Pytest
* **API Docs:** Swagger (OpenAPI)

---

## 📂 Project Structure

```
.
├── app/
│   ├── main.py          # FastAPI app & routes
│   ├── db.py            # Database connection
│   ├── schemas.py       # SQLAlchemy models
│   ├── ingestion.py     # ETL logic (API + CSV)
│
├── data/
│   └── crypto_prices.csv
│
├── tests/
│   └── test_api.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── Makefile
└── README.md
```

---

## ⚙️ Environment Variables

Create a `.env` file in the root directory:

```env
DATABASE_URL=postgresql://kasparro:kasparro@db:5432/kasparro_db
```

---

## 🐳 Running with Docker (Recommended)

### 1️⃣ Build & Start Services

```bash
docker compose up --build
```

### 2️⃣ API will be available at

* **API Base URL:** `http://localhost:8000`
* **Swagger Docs:** `http://localhost:8000/docs`

---

## 📡 API Endpoints

### ✅ Health Check

```
GET /health
```

Response:

```json
{
  "status": "ok",
  "database": "connected",
  "timestamp": 123456789,
  "request_id": "uuid"
}
```

---

### 📊 Get Crypto Data

```
GET /data?limit=10&offset=0
```

Response:

```json
{
  "request_id": "uuid",
  "api_latency_ms": 12,
  "count": 10,
  "data": [
    {
      "symbol": "BTC",
      "name": "Bitcoin",
      "price_usd": 88000,
      "source": "coinpaprika"
    }
  ]
}
```

---

### 📈 Ingestion Stats

```
GET /stats
```

Response:

```json
{
  "raw_records": 68,
  "normalized_records": 10,
  "sources": [
    {
      "source": "csv",
      "last_run": "2025-12-25T07:11:06Z"
    }
  ]
}
```

---

## 🔄 Data Ingestion Flow

* Runs automatically on application startup
* Steps:

  1. Fetch data from CoinPaprika API
  2. Load CSV data
  3. Store raw payloads
  4. Normalize into `crypto_assets`
  5. Update ETL checkpoints

---

## 🧪 Running Tests

```bash
pytest
```

---

## 🧠 Design Notes

* Separation of concerns (API, DB, ETL)
* Docker-first approach for consistency
* Simple schema for clarity and performance
* Swagger enabled for easy API testing

---

## ✅ Assignment Status

✔ All required features implemented
✔ Dockerized and reproducible
✔ APIs functional and documented
✔ Ready for evaluation

---

## 👤 Author

**Khushi Gupta**
Final Year Engineering Student
Backend Assignment Submissionpwd
