# 🚀 BACKEND START KARNE KA TARIKA

## ⚡ QUICK START (3 Steps)

### Step 1: Dependencies Install
```bash
cd "E:\Hackathon 5\The CRM Digital FTE Factory Final\backend"
pip install -r requirements.txt
```

### Step 2: Backend Start
**Option A**: Double-click `START.bat`

**Option B**: Command prompt me:
```bash
cd "E:\Hackathon 5\The CRM Digital FTE Factory Final\backend"
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Step 3: Test
Browser me kholo: **http://localhost:8000/docs**

---

## 📝 Complete Setup (Agar upar wala kaam na kare)

### 1. Command Prompt Kholo
- Windows + R dabao
- Type karo: `cmd`
- Enter dabao

### 2. Backend Directory Me Jao
```bash
cd E:\Hackathon 5\The CRM Digital FTE Factory Final\backend
```

### 3. Dependencies Install Karo
```bash
pip install fastapi uvicorn sqlalchemy asyncpg openai python-dotenv aiokafka python-multipart pydantic pydantic-settings httpx
```

### 4. Server Start Karo
```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Test Karo
Browser me: http://localhost:8000/docs

---

## ✅ Success Indicators

Agar server sahi se start hua toh yeh dikhega:

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx]
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

## 🐛 Common Errors & Fixes

### Error: `'uvicorn' is not recognized`
**Fix**: 
```bash
pip install uvicorn
```

### Error: `error parsing value for field "cors_origins"`
**Fix**: Already fixed in code! `.env` file me `CORS_ORIGINS` comma-separated hona chahiye.

### Error: `DATABASE_URL not found`
**Fix**: `.env` file already hai `backend/` directory me.

### Error: `Port 8000 already in use`
**Fix**: Different port use karo:
```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

### Error: `ModuleNotFoundError: No module named 'xxx'`
**Fix**: 
```bash
pip install -r requirements.txt
```

---

## 🎯 One-Liner Command

Copy-paste this in Command Prompt:

```bash
cd E:\Hackathon 5\The CRM Digital FTE Factory Final\backend && pip install fastapi uvicorn sqlalchemy asyncpg openai python-dotenv aiokafka python-multipart pydantic pydantic-settings httpx && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## 📞 Test Endpoints

Server start hone ke baad test karo:

1. **Health Check**: http://localhost:8000/health
2. **API Docs**: http://localhost:8000/docs
3. **Root**: http://localhost:8000

---

## 🎨 Frontend Start (Separate Terminal)

```bash
cd E:\Hackathon 5\The CRM Digital FTE Factory Final\forened
npm run dev
```

Frontend: http://localhost:3000

---

## ✨ Ready to Go!

Backend start hote hi:
- ✅ API ready hai
- ✅ Database connected hai (NeonDB)
- ✅ AI integration ready hai (Gemini)
- ✅ All endpoints working hain

**Phod do! 🚀🔥**
