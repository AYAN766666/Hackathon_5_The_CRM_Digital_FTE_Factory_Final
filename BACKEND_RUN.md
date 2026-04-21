# 🚀 Backend Setup & Run Guide

## Problem Fix

Agar `'uvicorn' is not recognized` error aa raha hai, toh yeh steps follow karo:

## ✅ Solution 1: Direct Pip Install (Recommended)

### Step 1: Dependencies Install
```bash
pip install fastapi uvicorn[standard] sqlalchemy[asyncio] asyncpg openai python-dotenv aiokafka python-multipart pydantic pydantic-settings httpx
```

### Step 2: Backend Run
```bash
cd "E:\Hackathon 5\The CRM Digital FTE Factory Final\backend"
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## ✅ Solution 2: Using Batch Files

### Setup (pehli baar):
```bash
# Project root me jao
cd "E:\Hackathon 5\The CRM Digital FTE Factory Final"

# Setup script run karo
setup.bat
```

### Rozana Run:
```bash
# Backend start karo
start-backend.bat
```

## ✅ Solution 3: Manual Steps

### Terminal 1 - Backend:
1. Open Command Prompt
2. Type:
```
cd /d E:\Hackathon 5\The CRM Digital FTE Factory Final\backend
```
3. Type:
```
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Terminal 2 - Frontend:
1. Open Command Prompt
2. Type:
```
cd /d E:\Hackathon 5\The CRM Digital FTE Factory Final\forened
```
3. Type:
```
npm run dev
```

## 🔍 Troubleshooting

### Error: `'uvicorn' is not recognized`
**Solution**: 
```bash
pip install uvicorn
```

### Error: `ModuleNotFoundError: No module named 'backend'`
**Solution**: Imports already fixed in the code. Ab direct import kaam karega.

### Error: `DATABASE_URL not found`
**Solution**: `backend/.env` file me DATABASE_URL already configured hai.

### Error: Port 8000 already in use
**Solution**: 
```bash
# Different port use karo
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

## ✅ Quick Test

Backend start hone ke baad, test karo:

```bash
curl http://localhost:8000/health
```

Ya browser me kholo:
- http://localhost:8000
- http://localhost:8000/docs

## 📝 Important Notes

1. **Python Path**: Python 3.9+ hona chahiye
2. **Dependencies**: Sab install hone chahiye
3. **.env file**: Backend directory me honi chahiye
4. **Port**: 8000 free hona chahiye

## 🎯 Complete Command (Copy-Paste)

```bash
# Install dependencies
pip install fastapi uvicorn sqlalchemy asyncpg openai python-dotenv aiokafka python-multipart pydantic pydantic-settings httpx

# Run backend
cd "E:\Hackathon 5\The CRM Digital FTE Factory Final\backend"
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

**Backend ready hai! 🚀**
