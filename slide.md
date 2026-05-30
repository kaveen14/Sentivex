# Sentivex — AI Customer Sentiment Analysis Dashboard
### Slide Deck

---

## Slide 1 — Title

# SENTIVEX
**AI-Powered Customer Sentiment Analysis Dashboard**

> Automatically classify customer feedback and visualize sentiment trends in real time.

| | |
|---|---|
| **Stack** | Python · PostgreSQL · Next.js |
| **Model** | BERT (Transformer-based NLP) |
| **Interface** | Interactive Real-Time Dashboard |

---

## Slide 2 — Problem Statement

### The Challenge

- Businesses receive thousands of customer reviews, tickets, and messages daily
- Manual classification is slow, inconsistent, and unscalable
- Delayed response to negative sentiment leads to churn
- No centralized view of emotional trends over time

```mermaid
graph LR
    A[Customer Feedback] -->|Manual Process| B[Slow Analysis]
    B --> C[Missed Issues]
    C --> D[Customer Churn]

    A -->|Sentivex| E[Automated NLP Pipeline]
    E --> F[Instant Classification]
    F --> G[Actionable Insights]
```

---

## Slide 3 — Solution Overview

### What Sentivex Does

```mermaid
flowchart TD
    Input["📥 Customer Feedback\n(text, reviews, tickets)"]
    Preprocess["🔧 NLP Preprocessing\n(tokenization, cleaning)"]
    Model["🤖 BERT Sentiment Model\n(Positive / Negative / Neutral)"]
    API["⚡ FastAPI Inference Layer"]
    DB["🗄️ PostgreSQL Database"]
    Dashboard["📊 Next.js Dashboard\n(trends, alerts, filters)"]

    Input --> Preprocess --> Model --> API --> DB --> Dashboard
```

---

## Slide 4 — System Architecture

### High-Level Architecture

```mermaid
C4Context
    title Sentivex — System Architecture

    Person(user, "Analyst / Business User", "Views sentiment trends on dashboard")

    System_Boundary(sentivex, "Sentivex Platform") {
        System(frontend, "Next.js Dashboard", "Real-time visualization & filters")
        System(api, "FastAPI Backend", "REST API for inference & data access")
        System(nlp, "NLP Pipeline", "Text preprocessing & BERT model")
        SystemDb(db, "PostgreSQL", "Stores feedback, predictions, metadata")
    }

    System_Ext(sources, "Feedback Sources", "CRM, emails, app reviews, chat logs")

    sources --> api
    user --> frontend
    frontend --> api
    api --> nlp
    api --> db
    nlp --> db
```

---

## Slide 5 — NLP Pipeline

### Text Preprocessing Flow

```mermaid
flowchart LR
    Raw["Raw Text\n'Product is great!! 😊'"]
    Clean["Clean Text\nLowercase, remove noise"]
    Token["Tokenized\n['product', 'great']"]
    Embed["BERT Embeddings\n[768-dim vectors]"]
    Classify["Classification\nPositive: 94%\nNeutral: 4%\nNegative: 2%"]

    Raw --> Clean --> Token --> Embed --> Classify

    style Classify fill:#22c55e,color:#fff
```

**Steps:**
1. HTML/emoji stripping, lowercasing
2. Punctuation normalization
3. HuggingFace BERT tokenizer (`bert-base-uncased`)
4. Softmax classification head (3 classes)

---

## Slide 6 — BERT Model Architecture

### Transformer-Based Sentiment Classifier

```mermaid
graph TD
    subgraph Input
        T["Input Tokens\n[CLS] product is great [SEP]"]
    end

    subgraph BERT["BERT Encoder (12 Layers)"]
        E["Token Embeddings"]
        A1["Multi-Head Attention × 12"]
        FF["Feed-Forward Layers"]
        CLS["[CLS] Representation\n(768-dim)"]
    end

    subgraph Head["Classification Head"]
        Drop["Dropout (0.3)"]
        Linear["Linear Layer (768 → 3)"]
        Soft["Softmax"]
    end

    Output["Sentiment Label + Confidence Score"]

    T --> E --> A1 --> FF --> CLS --> Drop --> Linear --> Soft --> Output
```

---

## Slide 7 — API Design

### RESTful Inference API (FastAPI)

```mermaid
sequenceDiagram
    participant Client as Next.js Frontend
    participant API as FastAPI Service
    participant NLP as BERT Model
    participant DB as PostgreSQL

    Client->>API: POST /api/v1/analyze { text, source }
    API->>NLP: Preprocess + Infer
    NLP-->>API: { label, confidence, scores }
    API->>DB: INSERT feedback + prediction
    DB-->>API: record_id
    API-->>Client: { id, sentiment, confidence, timestamp }

    Client->>API: GET /api/v1/trends?period=7d
    API->>DB: SELECT aggregated trends
    DB-->>API: trend data
    API-->>Client: { positive%, negative%, neutral%, timeline }
```

---

## Slide 8 — Database Schema

### PostgreSQL Entity Model

```mermaid
erDiagram
    FEEDBACK {
        uuid id PK
        text raw_text
        text cleaned_text
        varchar source
        timestamptz created_at
    }

    PREDICTION {
        uuid id PK
        uuid feedback_id FK
        varchar sentiment
        float confidence
        float score_positive
        float score_negative
        float score_neutral
        timestamptz predicted_at
    }

    SOURCE {
        uuid id PK
        varchar name
        varchar type
        boolean active
    }

    FEEDBACK ||--|| PREDICTION : "has"
    FEEDBACK }o--|| SOURCE : "from"
```

---

## Slide 9 — Dashboard Features

### Next.js Interactive Dashboard

```mermaid
mindmap
  root((Sentivex Dashboard))
    Overview
      Sentiment Donut Chart
      Daily Volume Bar Chart
      Live Confidence Score
    Trend Analysis
      7d / 30d / 90d Filters
      Positive vs Negative Timeline
      Moving Average Line
    Issue Detection
      Negative Spike Alerts
      Keyword Word Cloud
      Low-Confidence Flagging
    Data Management
      Search & Filter Feedback
      Export CSV / JSON
      Source Breakdown
```

---

## Slide 10 — Technology Stack

### Stack Summary

```mermaid
graph TD
    subgraph Frontend
        NX["Next.js 14\n(App Router)"]
        RC["React Components"]
        CH["Recharts / Chart.js"]
        TW["Tailwind CSS"]
    end

    subgraph Backend
        FA["FastAPI (Python)"]
        HF["HuggingFace Transformers"]
        PT["PyTorch"]
        SC["Scikit-learn"]
    end

    subgraph Data
        PG["PostgreSQL 16"]
        AQ["SQLAlchemy ORM"]
        RD["Redis (Optional Cache)"]
    end

    subgraph DevOps
        DK["Docker + Compose"]
        GH["GitHub Actions CI/CD"]
        NX2["Nginx Reverse Proxy"]
    end

    Frontend <--> Backend
    Backend <--> Data
    DevOps --> Frontend
    DevOps --> Backend
    DevOps --> Data
```

---

## Slide 11 — Deployment Architecture

```mermaid
graph LR
    subgraph Client
        Browser["User Browser"]
    end

    subgraph Server["Docker Host"]
        Nginx["Nginx\n:80 / :443"]
        NextApp["Next.js\n:3000"]
        FastAPI["FastAPI\n:8000"]
        PG["PostgreSQL\n:5432"]
    end

    Browser --> Nginx
    Nginx --> NextApp
    Nginx --> FastAPI
    FastAPI --> PG
```

---

## Slide 12 — Key Metrics & Goals

| Metric | Target |
|---|---|
| Sentiment Accuracy | ≥ 90% (F1) |
| API Response Time | < 300ms (p95) |
| Dashboard Load Time | < 1.5s |
| Data Ingestion Rate | 100 req/s |
| Model: Precision | ≥ 88% per class |

---

## Slide 13 — Project Roadmap

```mermaid
gantt
    title Sentivex Development Roadmap
    dateFormat  YYYY-MM-DD
    section Phase 1 — Foundation
    Project Setup & Scaffolding     :done,    p1a, 2026-05-29, 7d
    PostgreSQL Schema Design        :done,    p1b, 2026-05-29, 5d
    section Phase 2 — ML Pipeline
    NLP Preprocessing Module        :active,  p2a, 2026-06-05, 7d
    BERT Model Integration          :         p2b, 2026-06-10, 10d
    Model Fine-tuning               :         p2c, 2026-06-15, 7d
    section Phase 3 — Backend API
    FastAPI Setup & Endpoints       :         p3a, 2026-06-20, 7d
    DB Integration (SQLAlchemy)     :         p3b, 2026-06-24, 5d
    section Phase 4 — Frontend
    Next.js Dashboard Scaffold      :         p4a, 2026-06-27, 7d
    Chart & Trend Views             :         p4b, 2026-07-04, 7d
    section Phase 5 — Delivery
    Testing & QA                    :         p5a, 2026-07-10, 5d
    Docker Compose Deployment       :         p5b, 2026-07-13, 4d
    Demo & Documentation            :         p5c, 2026-07-17, 3d
```

---

## Slide 14 — Summary

### Sentivex Delivers

- **Automated** sentiment classification at scale with BERT
- **Real-time** inference via a low-latency FastAPI service
- **Persistent** storage of all feedback and predictions in PostgreSQL
- **Interactive** trends dashboard built with Next.js
- **Actionable** alerts for negative sentiment spikes

> Built to help businesses listen better, respond faster, and improve customer experience.
