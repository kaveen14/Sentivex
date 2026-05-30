# Sentivex

AI-powered Customer Sentiment Analysis Dashboard

## Quick Start

### Prerequisites
- Python 3.11+, Node.js 20+, Docker & Docker Compose

### Run with Docker Compose
```bash
docker compose up --build
```
- Dashboard → http://localhost
- API docs  → http://localhost/docs

---

### Local Development

**Backend**
```bash
cd backend
python -m venv .venv && .venv\Scripts\activate   # Windows
pip install -r requirements.txt
python -m spacy download en_core_web_sm
cp .env.example .env                              # Edit DATABASE_URL
python app/db/init_db.py                          # Init + seed DB
uvicorn app.main:app --reload
```

**Frontend**
```bash
cd frontend
npm install
cp .env.local.example .env.local
npm run dev
```

---

### Run Tests

**Backend**
```bash
cd backend
pytest
```

**Frontend**
```bash
cd frontend
npm test
```

---

### Fine-tune the BERT Model
```bash
cd backend
python -c "
from ml.trainer import SentimentTrainer
t = SentimentTrainer(output_dir='models/bert-sentiment')
t.train('path/to/your/dataset.csv')
"
```
CSV must have columns: `text` (str), `label` (int: 0=Negative, 1=Neutral, 2=Positive).

---

### Project Structure
```
sentivex/
├── backend/          FastAPI + BERT NLP pipeline
├── frontend/         Next.js dashboard
├── docker-compose.yml
├── nginx.conf
├── slide.md          Presentation deck
├── spec.md           Technical specification
└── Todo.md           Task tracker
```
