# Sentivex — Technical Specification

**Version:** 1.0.0  
**Date:** 2026-05-29  
**Status:** Draft  

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [System Architecture](#2-system-architecture)
3. [NLP Pipeline](#3-nlp-pipeline)
4. [Sentiment Model](#4-sentiment-model)
5. [Backend API](#5-backend-api)
6. [Database Design](#6-database-design)
7. [Frontend Dashboard](#7-frontend-dashboard)
8. [Data Flow](#8-data-flow)
9. [Security & Non-Functional Requirements](#9-security--non-functional-requirements)
10. [Deployment](#10-deployment)

---

## 1. Project Overview

### 1.1 Purpose

Sentivex is an AI-powered customer sentiment analysis platform that ingests free-text customer feedback, classifies each entry as **Positive**, **Negative**, or **Neutral** using a transformer-based NLP model, and presents results through an interactive real-time dashboard.

### 1.2 Scope

| In Scope | Out of Scope |
|---|---|
| Text sentiment classification (3-class) | Voice/audio sentiment analysis |
| REST API for single and batch inference | Multi-language support (v1) |
| PostgreSQL persistence layer | Real-time streaming (Kafka) |
| Next.js interactive dashboard | Mobile native app |
| Docker-based local deployment | Cloud auto-scaling (v1) |

### 1.3 Stakeholders

- **Product Owners** — Define business KPIs and feedback sources
- **Data Scientists** — Own NLP pipeline and model fine-tuning
- **Backend Engineers** — Implement FastAPI services and DB layer
- **Frontend Engineers** — Build Next.js dashboard
- **Analysts / Business Users** — Consume the dashboard

---

## 2. System Architecture

### 2.1 Component Overview

```mermaid
graph TB
    subgraph Sources["Feedback Sources"]
        S1["CRM System"]
        S2["App Reviews"]
        S3["Support Tickets"]
        S4["Manual Input"]
    end

    subgraph Backend["FastAPI Backend (Python)"]
        Router["API Router"]
        Preprocessor["NLP Preprocessor"]
        Model["BERT Classifier"]
        ORM["SQLAlchemy ORM"]
    end

    subgraph Storage["PostgreSQL 16"]
        FB["feedback"]
        PR["predictions"]
        SR["sources"]
    end

    subgraph Frontend["Next.js 14 (React)"]
        Overview["Overview Page"]
        Trends["Trends Page"]
        Issues["Issues Page"]
        Explorer["Data Explorer"]
    end

    Sources --> Router
    Router --> Preprocessor --> Model --> ORM --> Storage
    Router --> ORM
    Frontend --> Router
```

### 2.2 Layer Responsibilities

| Layer | Technology | Responsibility |
|---|---|---|
| Ingestion | FastAPI POST endpoints | Accept feedback from any source |
| Preprocessing | Python / spaCy | Clean, normalize, tokenize text |
| Inference | HuggingFace + PyTorch | Run BERT and produce label + confidence |
| Persistence | PostgreSQL + SQLAlchemy | Store all raw and enriched data |
| API | FastAPI + Pydantic | Expose REST endpoints to dashboard |
| Presentation | Next.js + Recharts | Visualize trends, alerts, raw data |

---

## 3. NLP Pipeline

### 3.1 Preprocessing Steps

```mermaid
flowchart TD
    A["Raw Input Text"]
    B["Strip HTML tags & URLs"]
    C["Decode HTML entities"]
    D["Remove special characters\n(retain punctuation for sentiment)"]
    E["Lowercase normalization"]
    F["Whitespace normalization"]
    G["HuggingFace BERT Tokenizer\n(max_length=512, truncation=True)"]
    H["Token IDs + Attention Mask"]

    A --> B --> C --> D --> E --> F --> G --> H
```

### 3.2 Preprocessing Rules

| Rule | Detail |
|---|---|
| Max token length | 512 (BERT limit) |
| Truncation strategy | `longest_first` |
| Padding | `max_length` for batch inference |
| Emoji handling | Stripped (v1); converted to text description (v2) |
| Language detection | English only — reject non-English (HTTP 422) |

### 3.3 Module Structure

```
backend/
└── nlp/
    ├── preprocessor.py     # TextPreprocessor class
    ├── tokenizer.py        # BERTTokenizerWrapper
    └── utils.py            # Regex patterns, language detection
```

---

## 4. Sentiment Model

### 4.1 Model Architecture

```mermaid
graph TD
    subgraph BERT["bert-base-uncased (HuggingFace)"]
        EMB["Embedding Layer\n(Vocab: 30,522 tokens)"]
        ENC["12× Transformer Encoder Blocks\n(768 hidden, 12 heads)"]
        CLS["[CLS] Pooled Output\n(768-dim vector)"]
    end

    subgraph Head["Classification Head"]
        DO["Dropout (p=0.3)"]
        LN["Linear (768 → 3)"]
        SM["Softmax"]
    end

    Labels["Output:\nPositive | Neutral | Negative\n+ Confidence Score"]

    EMB --> ENC --> CLS --> DO --> LN --> SM --> Labels
```

### 4.2 Model Specification

| Parameter | Value |
|---|---|
| Base model | `bert-base-uncased` |
| Fine-tuning dataset | SST-2 / custom customer feedback corpus |
| Output classes | 3 (Positive, Neutral, Negative) |
| Loss function | CrossEntropyLoss |
| Optimizer | AdamW (lr=2e-5, weight_decay=0.01) |
| Max epochs | 10 (with early stopping, patience=3) |
| Batch size | 16 (train), 32 (inference) |
| Dropout | 0.3 |

### 4.3 Model Evaluation Targets

| Metric | Target |
|---|---|
| Overall Accuracy | ≥ 90% |
| Macro F1 Score | ≥ 88% |
| Precision (per class) | ≥ 87% |
| Recall (per class) | ≥ 87% |

### 4.4 Model Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Pretrained : Load bert-base-uncased
    Pretrained --> FineTuning : Custom feedback dataset
    FineTuning --> Evaluation : Validation set scoring
    Evaluation --> Registered : Pass threshold (F1 ≥ 0.88)
    Evaluation --> FineTuning : Fail — adjust hyperparams
    Registered --> Serving : Load into FastAPI
    Serving --> Monitoring : Track prediction drift
    Monitoring --> FineTuning : Drift detected
```

---

## 5. Backend API

### 5.1 Base URL

```
http://localhost:8000/api/v1
```

### 5.2 Endpoints

#### `POST /analyze`
Analyze a single piece of feedback.

**Request Body:**
```json
{
  "text": "The product exceeded all my expectations!",
  "source": "app_review",
  "metadata": { "user_id": "optional", "region": "optional" }
}
```

**Response:**
```json
{
  "id": "uuid",
  "sentiment": "Positive",
  "confidence": 0.94,
  "scores": { "positive": 0.94, "neutral": 0.04, "negative": 0.02 },
  "timestamp": "2026-05-29T10:30:00Z"
}
```

#### `POST /analyze/batch`
Analyze multiple entries in one request (max 100).

#### `GET /feedback`
List paginated feedback with optional filters (`source`, `sentiment`, `from`, `to`).

#### `GET /trends`
Aggregated sentiment counts grouped by time period.

**Query params:** `period` (1d, 7d, 30d, 90d), `source`

**Response:**
```json
{
  "period": "7d",
  "summary": { "positive": 1402, "neutral": 310, "negative": 88 },
  "timeline": [
    { "date": "2026-05-23", "positive": 200, "neutral": 42, "negative": 12 }
  ]
}
```

#### `GET /health`
Service health check. Returns `{ "status": "ok", "model_loaded": true }`.

### 5.3 API Flow

```mermaid
sequenceDiagram
    participant C as Client (Next.js)
    participant R as FastAPI Router
    participant V as Pydantic Validator
    participant P as NLP Preprocessor
    participant M as BERT Model
    participant D as PostgreSQL

    C->>R: POST /api/v1/analyze
    R->>V: Validate input schema
    V-->>R: Validated payload
    R->>P: preprocess(text)
    P-->>R: tokens, attention_mask
    R->>M: infer(tokens)
    M-->>R: label, confidence, scores
    R->>D: INSERT feedback + prediction
    D-->>R: record_id
    R-->>C: 200 OK — sentiment response
```

### 5.4 Error Codes

| Code | Meaning |
|---|---|
| 422 | Invalid input (non-English, empty text, >10,000 chars) |
| 429 | Rate limit exceeded (100 req/min per IP) |
| 503 | Model not loaded / warming up |
| 500 | Internal inference error |

---

## 6. Database Design

### 6.1 Entity Relationship Diagram

```mermaid
erDiagram
    SOURCE {
        uuid id PK
        varchar name
        varchar type
        boolean active
        timestamptz created_at
    }

    FEEDBACK {
        uuid id PK
        uuid source_id FK
        text raw_text
        text cleaned_text
        varchar language
        jsonb metadata
        timestamptz created_at
    }

    PREDICTION {
        uuid id PK
        uuid feedback_id FK
        varchar sentiment
        float confidence
        float score_positive
        float score_neutral
        float score_negative
        varchar model_version
        timestamptz predicted_at
    }

    TREND_CACHE {
        uuid id PK
        varchar period
        date bucket_date
        int count_positive
        int count_neutral
        int count_negative
        timestamptz computed_at
    }

    SOURCE ||--o{ FEEDBACK : "generates"
    FEEDBACK ||--|| PREDICTION : "has one"
```

### 6.2 Indexes

| Table | Index | Type | Reason |
|---|---|---|---|
| `feedback` | `created_at` | BRIN | Range queries on date |
| `feedback` | `source_id` | BTREE | Filter by source |
| `prediction` | `sentiment` | BTREE | Filter by label |
| `prediction` | `predicted_at` | BRIN | Trend time queries |
| `prediction` | `confidence` | BTREE | Flag low-confidence |

### 6.3 Migrations

Managed with **Alembic**. All schema changes must go through versioned migration scripts under `backend/migrations/`.

---

## 7. Frontend Dashboard

### 7.1 Page Structure

```mermaid
graph TD
    App["Next.js App (App Router)"]

    App --> Layout["Root Layout\n(Navbar, Sidebar)"]
    Layout --> Overview["/dashboard\nOverview Page"]
    Layout --> Trends["/dashboard/trends\nTrend Analysis"]
    Layout --> Issues["/dashboard/issues\nIssue Detection"]
    Layout --> Explorer["/dashboard/explorer\nData Explorer"]
    Layout --> Ingest["/dashboard/ingest\nManual Feedback Input"]

    Overview --> C1["Sentiment Donut Chart"]
    Overview --> C2["Daily Volume Bar Chart"]
    Overview --> C3["KPI Summary Cards"]

    Trends --> C4["Multi-line Timeline Chart"]
    Trends --> C5["Period Selector (1d/7d/30d)"]

    Issues --> C6["Negative Spike Alert Feed"]
    Issues --> C7["Keyword Word Cloud"]
    Issues --> C8["Low-Confidence Flag Table"]

    Explorer --> C9["Paginated Feedback Table"]
    Explorer --> C10["Filter & Search Controls"]
    Explorer --> C11["CSV / JSON Export"]
```

### 7.2 Component Library

| Component | Library | Purpose |
|---|---|---|
| Line/Bar/Donut charts | Recharts | Trend and volume visualization |
| Data tables | TanStack Table | Sortable, filterable feedback list |
| Word cloud | `react-wordcloud` | Keyword frequency display |
| UI primitives | shadcn/ui + Tailwind | Consistent design system |
| API client | Axios + React Query | Data fetching with caching |
| Date picker | `react-day-picker` | Period filter controls |

### 7.3 State Management

- **Server state:** React Query (TanStack Query) — caches API responses, auto-refetches every 30s
- **UI state:** React `useState` / `useReducer` — local filter, sort, modal state
- **No global state library** required for v1

---

## 8. Data Flow

### 8.1 End-to-End Sentiment Flow

```mermaid
flowchart LR
    subgraph Ingestion
        Raw["Customer Text"]
        POST["POST /api/v1/analyze"]
    end

    subgraph Processing
        Clean["Text Cleaning"]
        Token["BERT Tokenization"]
        Infer["Model Inference"]
        Score["Score + Label"]
    end

    subgraph Persistence
        SaveFB["Save Feedback Record"]
        SavePR["Save Prediction Record"]
    end

    subgraph Presentation
        API["GET /api/v1/trends"]
        Chart["Dashboard Chart Update"]
    end

    Raw --> POST --> Clean --> Token --> Infer --> Score --> SaveFB --> SavePR
    SavePR --> API --> Chart
```

### 8.2 Dashboard Refresh Cycle

```mermaid
sequenceDiagram
    participant U as User
    participant D as Dashboard (Next.js)
    participant Q as React Query Cache
    participant A as FastAPI

    U->>D: Load /dashboard
    D->>Q: Check cache (stale?)
    Q->>A: GET /trends?period=7d
    A-->>Q: Trend data
    Q-->>D: Render charts
    Note over Q: Auto-refetch every 30s
    Q->>A: GET /trends (background refresh)
    A-->>Q: Updated data
    Q-->>D: Re-render if changed
```

---

## 9. Security & Non-Functional Requirements

### 9.1 Security

| Concern | Mitigation |
|---|---|
| Input validation | Pydantic schema validation on all endpoints |
| SQL injection | SQLAlchemy ORM with parameterized queries |
| XSS | Next.js automatic output escaping |
| Rate limiting | `slowapi` middleware (100 req/min per IP) |
| CORS | Whitelist only `localhost:3000` in development |
| Secrets | Environment variables via `.env` — never hardcoded |

### 9.2 Performance Targets

| Metric | Target |
|---|---|
| Single inference latency | < 300ms (p95) |
| Batch inference (100 items) | < 3s |
| Dashboard initial load | < 1.5s |
| Trend API response | < 200ms (with DB index) |
| Max concurrent requests | 50 (single instance) |

### 9.3 Scalability Notes

- BERT inference is CPU/GPU bound — use `torch.no_grad()` and model caching
- Model is loaded **once at startup** (singleton pattern) — not per-request
- For horizontal scaling, stateless API + shared PostgreSQL works without modification

---

## 10. Deployment

### 10.1 Docker Compose Services

```mermaid
graph TD
    subgraph docker-compose.yml
        NX["nextjs\nPort: 3000"]
        FA["fastapi\nPort: 8000"]
        PG["postgres\nPort: 5432"]
        NG["nginx\nPort: 80"]
    end

    NG --> NX
    NG --> FA
    FA --> PG
```

### 10.2 Environment Variables

**FastAPI (`backend/.env`):**

```
DATABASE_URL=postgresql://sentivex:password@postgres:5432/sentivex
MODEL_PATH=./models/bert-sentiment
MAX_BATCH_SIZE=100
RATE_LIMIT=100/minute
```

**Next.js (`frontend/.env.local`):**

```
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

### 10.3 Project Directory Structure

```
sentivex/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app entry point
│   │   ├── routers/
│   │   │   ├── analyze.py       # /analyze endpoints
│   │   │   └── trends.py        # /trends, /feedback endpoints
│   │   ├── models/
│   │   │   ├── db_models.py     # SQLAlchemy table definitions
│   │   │   └── schemas.py       # Pydantic request/response schemas
│   │   ├── services/
│   │   │   ├── sentiment.py     # Inference orchestration
│   │   │   └── trend_service.py # Aggregation queries
│   │   └── db/
│   │       ├── session.py       # DB session factory
│   │       └── init_db.py       # Schema bootstrap
│   ├── nlp/
│   │   ├── preprocessor.py
│   │   ├── tokenizer.py
│   │   └── utils.py
│   ├── ml/
│   │   ├── model.py             # BERTSentimentClassifier
│   │   ├── trainer.py           # Fine-tuning script
│   │   └── evaluate.py          # Metrics computation
│   ├── migrations/              # Alembic migration scripts
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── dashboard/
│   │   │   ├── page.tsx         # Overview
│   │   │   ├── trends/page.tsx
│   │   │   ├── issues/page.tsx
│   │   │   └── explorer/page.tsx
│   ├── components/
│   │   ├── charts/
│   │   ├── tables/
│   │   └── ui/
│   ├── lib/
│   │   ├── api.ts               # Axios API client
│   │   └── hooks/               # React Query hooks
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml
├── nginx.conf
├── slide.md
├── spec.md
└── Todo.md
```
