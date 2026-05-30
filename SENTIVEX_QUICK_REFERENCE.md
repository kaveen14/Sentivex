# Sentivex Quick Reference Guide

## 📋 Documentation Files Available

Two comprehensive documentation files have been created:

### 1. **SENTIVEX_PROJECT_DOCUMENTATION.md** (Markdown Format)
- Location: `c:\ProjectItem1\Sentivex\SENTIVEX_PROJECT_DOCUMENTATION.md`
- Best for: Viewing in GitHub, VS Code, or Markdown viewers
- Features: Formatted with headers, tables, code blocks, syntax highlighting
- Use this for: Development reference, online viewing

### 2. **SENTIVEX_PROJECT_DOCUMENTATION.txt** (Plain Text Format)
- Location: `c:\ProjectItem1\Sentivex\SENTIVEX_PROJECT_DOCUMENTATION.txt`
- Best for: Download, email, compatibility with any text editor
- Features: Easy to read, no special formatting required
- Use this for: Sharing, archiving, printing

---

## 🚀 Quick Start Commands

### Backend (Terminal 1)
```powershell
cd c:\ProjectItem1\Sentivex\backend
.\venv_new\Scripts\Activate.ps1
$env:DATABASE_URL = "sqlite:///./sentivex.db"
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend (Terminal 2)
```powershell
cd c:\ProjectItem1\Sentivex\frontend
npm run dev
```

### Access
- **Dashboard:** http://localhost:3002/dashboard
- **API:** http://localhost:8000/api/v1
- **Docs:** http://localhost:8000/docs

---

## 🗄️ Database Info

**Type:** SQLite (Development)  
**Location:** `backend/sentivex.db`  
**Tables:** sources, feedback, predictions

View database:
```powershell
cd c:\ProjectItem1\Sentivex\backend
sqlite3 sentivex.db
```

---

## 📊 Project Structure

```
Sentivex/
├── backend/
│   ├── app/
│   │   ├── main.py (FastAPI app entry)
│   │   ├── routers/ (API endpoints)
│   │   ├── models/ (Database & schemas)
│   │   ├── services/ (Business logic)
│   │   └── db/ (Database session)
│   ├── ml/ (ML training)
│   ├── nlp/ (NLP processing)
│   ├── tests/ (Unit tests)
│   ├── venv_new/ (Virtual environment)
│   └── requirements.txt
├── frontend/
│   ├── app/ (Next.js pages)
│   ├── components/ (React components)
│   ├── lib/ (Utilities)
│   └── package.json
└── Documentation files
```

---

## 🔑 Key Technologies

| Component | Technology | Version |
|-----------|-----------|---------|
| Backend | FastAPI | 0.111.0 |
| Frontend | Next.js | 15.5.18 |
| Python | Python | 3.11.9 |
| ML Model | BERT | bert-base-uncased |
| Database | SQLite | Latest |

---

## 🧪 Testing

Backend:
```powershell
cd backend
pytest tests/ -v
```

Frontend:
```powershell
cd frontend
npm test
```

---

## 📝 API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/v1/health` | Check API status |
| POST | `/api/v1/analyze` | Analyze single text |
| POST | `/api/v1/analyze/batch` | Batch analysis |
| GET | `/api/v1/trends` | Get trends |
| GET | `/api/v1/feedback` | List feedback |

---

## 🐛 Common Issues

**Port 8000 in use:**
```powershell
netstat -ano | findstr ":8000"
taskkill /PID <PID> /F
```

**API not responding:**
```powershell
curl http://localhost:8000/api/v1/health
```

**Frontend connection error:**
- Verify backend running on port 8000
- Check CORS configuration in `backend/app/main.py`

---

## 📥 How to Download Documentation

### Option 1: Download from File System
1. Navigate to: `c:\ProjectItem1\Sentivex\`
2. Right-click on `SENTIVEX_PROJECT_DOCUMENTATION.txt`
3. Select "Copy" or "Send to → Compressed folder"

### Option 2: Copy from Command Line
```powershell
copy "c:\ProjectItem1\Sentivex\SENTIVEX_PROJECT_DOCUMENTATION.txt" "$env:USERPROFILE\Downloads\Sentivex_Documentation.txt"
```

### Option 3: Email/Share
```powershell
# Both files are ready in:
# c:\ProjectItem1\Sentivex\SENTIVEX_PROJECT_DOCUMENTATION.md
# c:\ProjectItem1\Sentivex\SENTIVEX_PROJECT_DOCUMENTATION.txt
```

---

## 📚 Document Contents

The documentation includes:

- ✅ Project Overview
- ✅ Features List
- ✅ Technology Stack Details
- ✅ System Architecture Diagram
- ✅ Complete Database Schema
- ✅ Step-by-Step Installation Guide
- ✅ Running Instructions
- ✅ Full API Documentation with Examples
- ✅ Frontend Usage Guide
- ✅ Configuration Options
- ✅ Troubleshooting Section
- ✅ Deployment Guide (Docker, AWS, PostgreSQL)
- ✅ Security Best Practices
- ✅ Testing Guide
- ✅ Contributing Guidelines
- ✅ Glossary of Terms
- ✅ License Information
- ✅ Version History
- ✅ Contact Information

---

## 🎯 Current Status

| Component | Status | Port |
|-----------|--------|------|
| Backend API | ✅ Running | 8000 |
| Frontend Dashboard | ✅ Running | 3002 |
| Database | ✅ SQLite | - |
| BERT Model | ✅ Loaded | - |

---

## 📞 Need Help?

1. Check the **Troubleshooting** section in the documentation
2. Review **API Documentation** for endpoint details
3. Check **Configuration** for environment setup
4. Run **tests** to verify installation

---

## 🔄 Useful Commands

**View all services running:**
```powershell
netstat -ano | findstr ":3002\|:8000"
```

**Kill all Node processes:**
```powershell
taskkill /IM node.exe /F
```

**Reinstall backend dependencies:**
```powershell
cd backend
pip install -r requirements.txt --force-reinstall
```

**Clear frontend cache:**
```powershell
cd frontend
rm -r .next
npm run dev
```

---

## 📄 Files Created

1. **SENTIVEX_PROJECT_DOCUMENTATION.md** - Full markdown documentation
2. **SENTIVEX_PROJECT_DOCUMENTATION.txt** - Plain text version
3. **SENTIVEX_QUICK_REFERENCE.md** - This quick reference guide

All files are located in: `c:\ProjectItem1\Sentivex\`

---

**Last Updated:** May 30, 2026  
**Documentation Version:** 1.0.0  
**Status:** Complete ✅
