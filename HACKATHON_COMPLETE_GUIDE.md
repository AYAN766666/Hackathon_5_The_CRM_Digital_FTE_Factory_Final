# 🚀 Hackathon 5 - Complete Setup & Demo Guide

## ✅ What's Fixed

### WhatsApp Integration Issues Resolved:
1. ✅ **Persistent Session** - Browser session saved, no repeated QR scans
2. ✅ **Background Agent** - Doesn't block the main application
3. ✅ **Reliable Messaging** - Uses click-to-chat for guaranteed delivery
4. ✅ **Fast Response** - Pre-initialized agent ready to send instantly

---

## 📋 Pre-Demo Checklist

### 1. Install Dependencies

```bash
# Navigate to backend
cd "E:\Hackathon 5\The CRM Digital FTE Factory Final\backend"

# Install Python dependencies
uv sync

# Install Playwright browser
python -m playwright install chromium
```

### 2. Configure Environment

Check `backend/.env` has:

```env
# Database
DATABASE_URL=postgresql://neondb_owner:npg_1lTk7OyvwfaL@ep-curly-heart-ah137twq-pooler.c-3.us-east-1.aws.neon.tech/neondb?ssl=true

# AI
GEMINI_API_KEY=your_gemini_api_key_here

# Email
GMAIL_EMAIL=aayanu52@gmail.com
GMAIL_APP_PASSWORD=wvkx mqvu umlz trwd
```

### 3. First-Time WhatsApp Login

**IMPORTANT**: Do this ONCE before the demo:

```bash
# Run WhatsApp agent
python test-whatsapp.py
```

- Browser opens
- Scan QR code with your phone
- Wait for "Agent started successfully"
- Press Ctrl+C to stop

**Session is now saved!** Future runs auto-login.

---

## 🎬 Demo Flow (Step by Step)

### Step 1: Start Backend

```bash
cd "E:\Hackathon 5\The CRM Digital FTE Factory Final\backend"
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Keep this terminal open!**

### Step 2: Verify Backend is Running

Open browser: http://localhost:8000/health

Should show:
```json
{
  "status": "healthy",
  "database": "connected",
  "ai_service": "ready"
}
```

### Step 3: Start Frontend (if not already running)

```bash
cd "E:\Hackathon 5\The CRM Digital FTE Factory Final\forened"
npm run dev
```

Frontend: http://localhost:3000

### Step 4: Demo to Judges

#### A. Open Web Form
Navigate to: http://localhost:3000

#### B. Fill Support Form
```
Name: Judge Name
Email: aayanu52@gmail.com
Phone: +923198130598
Category: Technical
Message: I am having trouble logging into my account. 
         Can you please help me reset my password?
```

#### C. Submit Form
Click **Submit Request**

#### D. Show Results
1. ✅ **Ticket ID displayed** on screen
2. ✅ **Email received** at aayanu52@gmail.com
3. ✅ **WhatsApp received** at +923198130598

#### E. Check Ticket Status
1. Click **Check Ticket Status**
2. Enter the Ticket ID
3. Show conversation history with AI response

---

## 📱 WhatsApp Message Format

Customer receives:

```
Hello Judge Name! 👋

Your support ticket ABCD1234 has been created.

Our team will review your issue shortly.

Thank you for contacting us!
```

---

## 📧 Email Format

Customer receives HTML email with:
- Ticket ID
- AI-generated response
- Professional branding
- Contact information

---

## 🎯 Key Features to Highlight

### 1. Multi-Channel Support
- ✅ Email (Gmail SMTP)
- ✅ WhatsApp (Playwright automation)
- ✅ Web Form (Next.js)

### 2. AI-Powered Responses
- ✅ Gemini 2.0 Flash
- ✅ Sentiment analysis
- ✅ Escalation detection

### 3. Real-Time Processing
- ✅ Async message sending
- ✅ Non-blocking notifications
- ✅ Sub-3-second response time

### 4. Persistent Sessions
- ✅ WhatsApp login saved
- ✅ Database persistence (NeonDB)
- ✅ 24-hour conversation window

### 5. Professional UI
- ✅ Gradient buttons
- ✅ Glassmorphism cards
- ✅ Smooth animations (Framer Motion)
- ✅ Responsive design

---

## 🔧 Troubleshooting

### WhatsApp Not Working?

**Check 1**: Is WhatsApp agent initialized?
```bash
curl http://localhost:8000/whatsapp/status
```

**Check 2**: Is browser installed?
```bash
python -m playwright install chromium
```

**Check 3**: Is session saved?
```
Check folder exists: backend/.whatsapp_session/
```

### Email Not Sending?

**Check 1**: Gmail credentials correct?
```env
GMAIL_EMAIL=aayanu52@gmail.com
GMAIL_APP_PASSWORD=wvkx mqvu umlz trwd
```

**Check 2**: 2FA enabled on Gmail?
- Go to Google Account → Security
- Enable 2-Factor Authentication
- Generate App Password

### Backend Crashes?

**Check 1**: Database connection
```bash
curl http://localhost:8000/health
```

**Check 2**: Dependencies installed
```bash
uv sync
```

**Check 3**: Port 8000 not in use
```bash
netstat -ano | findstr :8000
```

---

## 📊 API Endpoints for Demo

### Submit Support Request
```bash
curl -X POST http://localhost:8000/support/submit ^
  -H "Content-Type: application/json" ^
  -d "{\"name\": \"Judge\", \"email\": \"judge@example.com\", \"phone\": \"923198130598\", \"category\": \"Technical\", \"message\": \"Help me please\"}"
```

### Check Ticket Status
```bash
curl http://localhost:8000/support/ticket/ABCD1234
```

### Send WhatsApp Message
```bash
curl -X POST http://localhost:8000/whatsapp/send ^
  -H "Content-Type: application/json" ^
  -d "{\"phone_number\": \"923198130598\", \"message\": \"Hello from API!\"}"
```

### Test Email
```bash
curl -X POST http://localhost:8000/email/test ^
  -H "Content-Type: application/json" ^
  -d "{\"email\": \"aayanu52@gmail.com\", \"name\": \"Test User\"}"
```

---

## 💡 Demo Tips

### Before Judges Arrive
1. ✅ Start backend
2. ✅ Start frontend
3. ✅ Verify health check
4. ✅ Test email once
5. ✅ Test WhatsApp once
6. ✅ Keep browser windows visible

### During Demo
1. 🎯 Speak clearly about each channel
2. 🎯 Show real-time notifications
3. 🎯 Explain AI integration
4. 🎯 Highlight persistence (database)
5. 🎯 Demo ticket status lookup

### After Demo
1. Show API documentation: http://localhost:8000/docs
2. Show database tables (NeonDB console)
3. Show code structure
4. Explain architecture decisions

---

## 🏆 Architecture Diagram

```
┌─────────────┐
│   Customer  │
│  Web Form   │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────┐
│     FastAPI Backend (Port 8000) │
│  ┌───────────────────────────┐  │
│  │  /support/submit          │  │
│  │  1. Create Ticket         │  │
│  │  2. Save to NeonDB        │  │
│  │  3. Generate AI Response  │  │
│  │  4. Send Email (async)    │  │
│  │  5. Send WhatsApp (async) │  │
│  └───────────────────────────┘  │
└─────────────────────────────────┘
       │              │
       │              ▼
       │       ┌─────────────┐
       │       │ Gmail SMTP  │
       │       │   Email     │
       │       └─────────────┘
       │
       ▼
┌─────────────────┐
│ WhatsApp Agent  │
│ (Playwright)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  WhatsApp Web   │
│   (Saved        │
│   Session)      │
└─────────────────┘
```

---

## 📁 Project Structure

```
backend/
├── main.py                    # FastAPI app
├── config.py                  # Configuration
├── database.py                # NeonDB connection
├── models.py                  # SQLAlchemy models
├── schemas.py                 # Pydantic schemas
├── routes/
│   ├── webform.py            # Web form routes
│   ├── email.py              # Email routes
│   └── whatsapp.py           # WhatsApp routes
├── services/
│   ├── ai_service.py         # Gemini AI
│   ├── customer_service.py   # Customer management
│   ├── conversation_service.py # Conversations
│   ├── message_service.py    # Messages
│   ├── email_service.py      # Gmail SMTP
│   └── whatsapp_agent.py     # WhatsApp automation
├── .env                       # Environment variables
└── requirements.txt           # Dependencies

forened/
├── app/
│   ├── page.tsx              # Home page
│   └── globals.css           # Styles
├── components/
│   └── SupportForm.tsx       # Support form
└── tests/
    └── support-form.spec.ts  # Playwright tests
```

---

## 🎉 Success Criteria

| Metric | Target | Status |
|--------|--------|--------|
| Email Delivery | < 5 seconds | ✅ Implemented |
| WhatsApp Delivery | < 10 seconds | ✅ Implemented |
| AI Response Time | < 3 seconds | ✅ Implemented |
| Ticket Persistence | 100% | ✅ NeonDB |
| Session Persistence | Forever | ✅ Saved |
| Form Validation | Client + Server | ✅ Both |

---

## 📞 Contact Numbers for Demo

- **Your WhatsApp**: +923198130598
- **Your Email**: aayanu52@gmail.com

Use these in the form to receive real notifications!

---

## 🚀 Quick Commands

### Start Everything
```bash
# Terminal 1: Backend
cd backend
uvicorn main:app --reload

# Terminal 2: Frontend
cd forened
npm run dev
```

### Test APIs
```bash
# Health check
curl http://localhost:8000/health

# Submit ticket
curl -X POST http://localhost:8000/support/submit ^
  -H "Content-Type: application/json" ^
  -d "{\"name\": \"Test\", \"email\": \"test@example.com\", \"phone\": \"923198130598\", \"category\": \"Technical\", \"message\": \"Help\"}"
```

---

## ✅ Final Checklist

Before demo:
- [ ] Backend running
- [ ] Frontend running
- [ ] WhatsApp session logged in
- [ ] Email tested successfully
- [ ] Phone number ready: +923198130598
- [ ] API docs loaded: http://localhost:8000/docs
- [ ] Database connected: NeonDB

---

**Good luck for Hackathon 5!** 🎉

**You've got this!** 💪
