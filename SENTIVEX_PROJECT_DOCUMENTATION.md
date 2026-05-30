# Sentivex: AI Sentiment Dashboard
## Professional Project Documentation

**Version:** 1.0.0  
**Date:** May 30, 2026  
**Status:** Production Ready

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Technology Stack](#technology-stack)
4. [System Architecture](#system-architecture)
5. [Database Schema](#database-schema)
6. [Installation & Setup](#installation--setup)
7. [Running the Project](#running-the-project)
8. [API Documentation](#api-documentation)
9. [Frontend Usage](#frontend-usage)
10. [Configuration](#configuration)
11. [Troubleshooting](#troubleshooting)
12. [Deployment Guide](#deployment-guide)

---

## Project Overview

### What is Sentivex?

Sentivex is an **AI-powered Sentiment Analysis Dashboard** that provides real-time sentiment analysis of user feedback and comments. It combines machine learning, natural language processing, and data visualization to deliver actionable insights about customer sentiment.

### Key Purpose

- Analyze customer feedback and social media comments
- Classify sentiment as Positive, Neutral, or Negative
- Track sentiment trends over time
- Provide visual dashboards for sentiment metrics
- Support batch processing of large feedback datasets

### Use Cases

- **Customer Service:** Monitor customer satisfaction
- **Social Media:** Analyze brand sentiment on social platforms
- **Product Feedback:** Understand product reviews and ratings
- **Market Research:** Track sentiment trends for competitive analysis
- **Quality Assurance:** Identify common complaints and issues

---

## Features

### Core Features

✅ **Real-Time Sentiment Analysis**
- Powered by BERT (Bidirectional Encoder Representations from Transformers)
- Supports English text analysis
- Confidence scores for each prediction

✅ **Sentiment Classification**
- Positive: Favorable feedback and compliments
- Neutral: Factual statements without emotion
- Negative: Complaints and critical feedback

✅ **Interactive Dashboard**
- Overview page with sentiment summary
- Sentiment distribution visualizations (pie charts)
- Daily feedback volume trends (line charts)
- Real-time KPI cards showing metrics

✅ **Data Management**
- Multi-source feedback ingestion
- Metadata support for custom fields
- Historical data tracking
- Time-series analytics

✅ **API Integration**
- RESTful API for programmatic access
- Rate limiting for protection
- CORS-enabled for cross-origin requests
- Batch processing support

✅ **Database**
- SQLite for development (lightweight, file-based)
- PostgreSQL support for production
- Relational schema with proper indexing

---

## Technology Stack

### Backend

| Component | Technology | Version |
|-----------|-----------|---------|
| **Framework** | FastAPI | 0.111.0 |
| **Server** | Uvicorn | 0.30.1 |
| **Language** | Python | 3.11.9 |
| **ORM** | SQLAlchemy | 2.0.30 |
| **Validation** | Pydantic | 2.7.1 |
| **ML Framework** | PyTorch | 2.3.0 |
| **NLP Model** | Transformers (BERT) | 4.41.2 |
| **Text Processing** | spaCy | >=3.8.0 |

### Frontend

| Component | Technology | Version |
|-----------|-----------|---------|
| **Framework** | Next.js | 15.5.18 |
| **Runtime** | Node.js | 25.2.1 |
| **Language** | TypeScript | 5.x |
| **Styling** | Tailwind CSS | 3.x |
| **HTTP Client** | Axios | Latest |
| **Testing** | Jest | Latest |

### Infrastructure

| Component | Technology |
|-----------|-----------|
| **Database (Dev)** | SQLite |
| **Database (Prod)** | PostgreSQL |
| **Container** | Docker |
| **Orchestration** | Docker Compose |
| **Web Server** | Nginx |

---

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Browser                             │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/HTTPS
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Nginx (Reverse Proxy)                      │
│              (Routes requests to services)                   │
└────────────────┬──────────────────────────────┬──────────────┘
                 │                              │
                 ▼                              ▼
    ┌──────────────────────┐      ┌──────────────────────────┐
    │  Next.js Frontend    │      │   FastAPI Backend API    │
    │  Port: 3002          │      │   Port: 8000             │
    │  (Dashboard UI)      │      │   (Data Processing)      │
    └──────────────────────┘      └─────────────┬────────────┘
                                                 │
                                                 ▼
                                  ┌──────────────────────────┐
                                  │  SQLite Database         │
                                  │  (sentivex.db)           │
                                  │  - Feedback              │
                                  │  - Predictions           │
                                  │  - Sources               │
                                  └──────────────────────────┘
```

### Request Flow

1. **User Action** → Frontend Dashboard
2. **API Request** → FastAPI Backend
3. **ML Processing** → BERT Sentiment Model
4. **Data Storage** → SQLite Database
5. **Response** → JSON Data
6. **Visualization** → Chart Components
7. **Display** → User Dashboard

### Component Breakdown

**Frontend (Next.js)**
- Renders user interface
- Handles client-side routing
- Makes API calls to backend
- Visualizes data with charts

**Backend (FastAPI)**
- Processes sentiment analysis requests
- Manages database operations
- Serves API endpoints
- Loads and runs BERT model

**Database (SQLite)**
- Stores feedback records
- Stores predictions and scores
- Tracks data sources
- Maintains history

**ML Model (BERT)**
- Pre-trained on 12 million sentences
- Fine-tuned for sentiment analysis
- Provides confidence scores
- Returns multi-class predictions

---

## Database Schema

### Tables Overview

#### 1. `sources` Table
Manages data sources for feedback.

```
sources
├─ id (UUID) [PRIMARY KEY]
├─ name (String, 100) - Source identifier (unique)
├─ type (String, 50) - Source type (e.g., "twitter", "email")
├─ active (Boolean) - Is source currently active?
└─ created_at (DateTime) - Source creation timestamp
```

#### 2. `feedback` Table
Stores raw feedback text and metadata.

```
feedback
├─ id (UUID) [PRIMARY KEY]
├─ source_id (UUID) [FOREIGN KEY → sources]
├─ raw_text (Text) - Original feedback text
├─ cleaned_text (Text) - Processed text after NLP
├─ language (String, 10) - Language code (default: "en")
├─ metadata (JSON) - Custom fields and tags
└─ created_at (DateTime) - When feedback was received
```

#### 3. `predictions` Table
Stores sentiment analysis results.

```
predictions
├─ id (UUID) [PRIMARY KEY]
├─ feedback_id (UUID) [FOREIGN KEY → feedback]
├─ sentiment (String, 20) - Classification: "positive", "neutral", "negative"
├─ confidence (Float) - Confidence score (0.0 - 1.0)
├─ score_positive (Float) - Probability score for positive
├─ score_neutral (Float) - Probability score for neutral
├─ score_negative (Float) - Probability score for negative
├─ model_version (String, 50) - Model used for prediction
└─ predicted_at (DateTime) - Prediction timestamp
```

### Entity Relationship Diagram

```
sources (1) ──── (M) feedback (1) ──── (1) predictions
   │                    │
   └─ id (UUID)         ├─ id (UUID)
   ├─ name              ├─ source_id (FK)
   └─ ...               └─ ...
                        
                        predictions
                        ├─ id (UUID)
                        ├─ feedback_id (FK)
                        ├─ sentiment
                        ├─ confidence
                        └─ score_*
```

---

## Installation & Setup

### Prerequisites

Before installation, ensure you have:

- **Python 3.11+** installed
- **Node.js 18+** installed
- **Git** for version control
- **4GB RAM** minimum (for BERT model loading)
- **2GB disk space** for dependencies and models

### Step 1: Clone Repository

```bash
cd c:\ProjectItem1
git clone https://github.com/yourusername/sentivex.git
cd Sentivex
```

### Step 2: Backend Setup

#### 2.1 Create Python Virtual Environment

```powershell
cd backend
python -m venv venv_new
.\venv_new\Scripts\Activate.ps1
```

#### 2.2 Install Python Dependencies

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

**Key Dependencies:**
- FastAPI: Web framework
- SQLAlchemy: ORM for database
- Transformers: BERT model library
- PyTorch: Deep learning framework
- spaCy: NLP preprocessing

#### 2.3 Initialize Database

```powershell
python -c "from app.db.init_db import init_db; init_db()"
```

This creates:
- SQLite database file (`sentivex.db`)
- All required tables
- Sample data for testing

### Step 3: Frontend Setup

#### 3.1 Install Node Dependencies

```powershell
cd ..\frontend
npm install
```

#### 3.2 Configure Environment (if needed)

Create `.env.local` file:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Step 4: Verify Installation

```powershell
# Test backend
python -m pytest backend/tests/ -v

# Test frontend
npm run test
```

---

## Running the Project

### Quick Start (Both Services)

#### Terminal 1 - Backend

```powershell
cd c:\ProjectItem1\Sentivex\backend
.\venv_new\Scripts\Activate.ps1
$env:DATABASE_URL = "sqlite:///./sentivex.db"
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
INFO:app.main:Sentivex API ready.
```

#### Terminal 2 - Frontend

```powershell
cd c:\ProjectItem1\Sentivex\frontend
npm run dev
```

**Expected Output:**
```
> sentivex-frontend@1.0.0 dev
> next dev
Ready in 2.5s
```

### Access the Application

- **Dashboard:** http://localhost:3002/dashboard
- **API Docs:** http://localhost:8000/docs
- **API (Interactive):** http://localhost:8000/redoc

### Production Build

#### Backend

```powershell
# Build Docker image
docker build -t sentivex-backend -f backend/Dockerfile .

# Run container
docker run -p 8000:8000 -e DATABASE_URL="postgresql://..." sentivex-backend
```

#### Frontend

```powershell
# Build Next.js
npm run build

# Start production server
npm start
```

---

## API Documentation

### Base URL

```
http://localhost:8000/api/v1
```

### Endpoints

#### 1. Health Check

**Endpoint:** `GET /health`

**Description:** Check API status and model status

**Response:**
```json
{
  "status": "ok",
  "model_loaded": true,
  "version": "1.0.0"
}
```

**cURL Example:**
```bash
curl http://localhost:8000/api/v1/health
```

---

#### 2. Analyze Single Feedback

**Endpoint:** `POST /analyze`

**Description:** Perform sentiment analysis on a single text

**Request Body:**
```json
{
  "text": "This product is amazing!",
  "source": "manual",
  "metadata": {
    "user_id": "123",
    "platform": "website"
  }
}
```

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "sentiment": "positive",
  "confidence": 0.95,
  "scores": {
    "positive": 0.95,
    "neutral": 0.03,
    "negative": 0.02
  },
  "timestamp": "2026-05-30T17:12:14Z"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "text": "I love this!",
    "source": "twitter"
  }'
```

---

#### 3. Analyze Batch Feedback

**Endpoint:** `POST /analyze/batch`

**Description:** Process multiple feedback items at once

**Request Body:**
```json
{
  "items": [
    {
      "text": "Great service!",
      "source": "email"
    },
    {
      "text": "Poor quality",
      "source": "review"
    }
  ]
}
```

**Response:**
```json
{
  "results": [
    {
      "id": "...",
      "sentiment": "positive",
      "confidence": 0.92,
      "scores": {...}
    },
    {
      "id": "...",
      "sentiment": "negative",
      "confidence": 0.88,
      "scores": {...}
    }
  ],
  "total": 2
}
```

---

#### 4. Get Trends

**Endpoint:** `GET /trends?period=7d`

**Description:** Get sentiment trends for a time period

**Query Parameters:**
- `period`: Time period (7d, 30d, 90d, 1y)

**Response:**
```json
{
  "period": "7d",
  "summary": {
    "positive": 28,
    "neutral": 15,
    "negative": 12,
    "total": 55
  },
  "timeline": [
    {
      "date": "2026-05-30",
      "positive": 5,
      "neutral": 2,
      "negative": 1
    }
  ]
}
```

---

#### 5. Get Feedback List

**Endpoint:** `GET /feedback?skip=0&limit=10`

**Description:** Retrieve stored feedback with pagination

**Query Parameters:**
- `skip`: Number of records to skip (default: 0)
- `limit`: Number of records to return (default: 10)

**Response:**
```json
[
  {
    "id": "...",
    "raw_text": "Excellent product",
    "sentiment": "positive",
    "confidence": 0.94,
    "source": "twitter",
    "created_at": "2026-05-30T17:12:14Z"
  }
]
```

---

### Error Handling

**Rate Limit Exceeded (429):**
```json
{
  "detail": "Rate limit exceeded. Maximum 100 requests per minute."
}
```

**Invalid Request (400):**
```json
{
  "detail": "Text must not be empty or whitespace only"
}
```

**Server Error (500):**
```json
{
  "detail": "Internal server error"
}
```

---

## Frontend Usage

### Dashboard Pages

#### 1. Overview Page (`/dashboard`)

**Components:**
- KPI Cards: Total Feedback, Positive %, Negative %, Neutral %
- Sentiment Distribution Pie Chart
- Daily Feedback Volume Line Chart

**Features:**
- Real-time data updates
- Color-coded sentiment indicators
- Responsive layout for mobile devices

#### 2. Trends Page (`/dashboard/trends`)

**Displays:**
- Weekly sentiment trends
- Historical comparison
- Growth/decline metrics

#### 3. Issues Page (`/dashboard/issues`)

**Shows:**
- Negative feedback items
- Common complaint patterns
- Priority ranking

#### 4. Explorer Page (`/dashboard/explorer`)

**Features:**
- Search and filter feedback
- Export to CSV
- Detailed sentiment breakdown

#### 5. Ingest Page (`/dashboard/ingest`)

**Actions:**
- Manually submit feedback
- Batch import from file
- Configure data sources

---

## Configuration

### Environment Variables

Create `.env` file in backend directory:

```env
# Database Configuration
DATABASE_URL=sqlite:///./sentivex.db
# For PostgreSQL: postgresql://user:password@localhost/sentivex

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3002

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_PERIOD=60

# Model Configuration
MODEL_NAME=bert-base-uncased
CACHE_DIR=./models
```

### CORS Settings

**File:** `backend/app/main.py`

```python
CORSMiddleware(
    app,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
```

---

## Troubleshooting

### Problem: Backend won't start

**Error:** `Port 8000 is already in use`

**Solution:**
```powershell
# Find process using port 8000
netstat -ano | findstr ":8000"

# Kill process (replace PID)
taskkill /PID <PID> /F

# Restart backend
python -m uvicorn app.main:app --reload --port 8000
```

---

### Problem: Frontend shows "API connection error"

**Error:** `Failed to load resource`

**Causes & Solutions:**

1. Backend not running:
```powershell
# Check if backend is running on port 8000
curl http://localhost:8000/api/v1/health
```

2. CORS policy blocks request:
   - Verify CORS configuration in `backend/app/main.py`
   - Add frontend URL to `allow_origins` list

3. Database not accessible:
```powershell
# Verify database file exists
ls backend/sentivex.db

# Reinitialize if missing
python backend/app/db/init_db.py
```

---

### Problem: BERT model download fails

**Error:** `Connection timeout when downloading model`

**Solution:**
```powershell
# Download manually
python -m spacy download en_core_web_sm

# Set cache directory
$env:TRANSFORMERS_CACHE="C:\path\to\cache"

# Retry startup
python -m uvicorn app.main:app --reload
```

---

### Problem: Out of memory when loading BERT

**Error:** `RuntimeError: CUDA out of memory`

**Solution:**
```python
# In backend/app/services/sentiment.py
# Use CPU instead of GPU
device = torch.device("cpu")  # Not "cuda"
model = model.to(device)
```

---

## Deployment Guide

### Docker Deployment

**1. Build Images:**
```bash
docker-compose build
```

**2. Run Services:**
```bash
docker-compose up -d
```

**3. Verify:**
```bash
docker-compose ps
curl http://localhost:8000/api/v1/health
```

### Cloud Deployment (AWS Example)

**1. Push to ECR:**
```bash
aws ecr get-login-password | docker login --username AWS
docker tag sentivex:latest <account>.dkr.ecr.<region>.amazonaws.com/sentivex:latest
docker push <account>.dkr.ecr.<region>.amazonaws.com/sentivex:latest
```

**2. Deploy to ECS:**
- Create task definition
- Create service
- Configure load balancer

### PostgreSQL Migration

**1. Update Database URL:**
```env
DATABASE_URL=postgresql://user:password@localhost/sentivex
```

**2. Create Database:**
```bash
createdb sentivex
```

**3. Run Migrations:**
```bash
alembic upgrade head
```

---

## Performance Optimization

### Backend Optimization

- **Model Caching:** Pre-load BERT model at startup
- **Batch Processing:** Process multiple items simultaneously
- **Connection Pooling:** Reuse database connections
- **Rate Limiting:** Prevent abuse (100 req/min)

### Frontend Optimization

- **Code Splitting:** Lazy load page components
- **Image Optimization:** Use Next.js Image component
- **Caching:** Browser cache for static assets
- **API Debouncing:** Limit API calls on user input

### Database Optimization

- **Indexing:** Index frequently queried columns
- **Query Optimization:** Use efficient SQL queries
- **Archiving:** Move old data to archive table
- **Partitioning:** Split large tables by date range

---

## Security Best Practices

### Authentication & Authorization

```python
# Add JWT authentication (example)
from fastapi.security import HTTPBearer
security = HTTPBearer()

@app.post("/analyze")
async def analyze(request: AnalyzeRequest, token: str = Depends(security)):
    # Validate token
    # Process request
    pass
```

### Data Protection

- ✅ Use HTTPS in production
- ✅ Hash sensitive data
- ✅ Encrypt database connection
- ✅ Sanitize user input
- ✅ Implement CSRF protection

### Rate Limiting

```python
# Already implemented in main.py
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@app.post("/analyze")
@limiter.limit("100/minute")
async def analyze(request: AnalyzeRequest):
    pass
```

---

## Testing

### Backend Testing

```bash
cd backend
pytest tests/ -v
pytest tests/ --cov=app  # With coverage
```

### Frontend Testing

```bash
cd frontend
npm test
npm run test:coverage
```

### Integration Testing

```bash
# Test API endpoints
pytest tests/test_api.py -v

# Test database operations
pytest tests/test_db.py -v

# Test ML model
pytest tests/test_model.py -v
```

---

## Support & Contributing

### Getting Help

- **Issues:** Report bugs on GitHub Issues
- **Discussions:** Ask questions on GitHub Discussions
- **Documentation:** Check API docs at `/docs`

### Contributing

1. Fork repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

### Development Workflow

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\Activate.ps1  # Windows

# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests before commit
pytest tests/ -v
black app/  # Format code
flake8 app/  # Lint code

# Submit PR
```

---

## Glossary

| Term | Definition |
|------|-----------|
| **BERT** | Bidirectional Encoder Representations from Transformers |
| **NLP** | Natural Language Processing |
| **CORS** | Cross-Origin Resource Sharing |
| **ORM** | Object-Relational Mapping |
| **FastAPI** | Modern Python web framework for APIs |
| **SQLAlchemy** | SQL toolkit and ORM library |
| **JWT** | JSON Web Token for authentication |
| **REST** | Representational State Transfer |
| **API** | Application Programming Interface |

---

## License

This project is licensed under the MIT License - see LICENSE file for details.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-05-30 | Initial release with BERT sentiment analysis |
| 0.9.0 | 2026-05-20 | Beta testing phase |
| 0.5.0 | 2026-05-01 | Alpha release |

---

## Contact

- **Author:** Sentivex Team
- **Email:** support@sentivex.com
- **Website:** https://sentivex.com
- **GitHub:** https://github.com/sentivex/sentivex

---

**Last Updated:** May 30, 2026  
**Document Version:** 1.0.0

