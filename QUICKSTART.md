# Quick Start Guide - Customer Success FTE

## 🚀 Quick Setup (5 minutes)

### Step 1: Setup Backend

```bash
# Navigate to backend
cd backend

# Create virtual environment
uv venv

# Activate (Windows)
.venv\Scripts\activate

# Install dependencies
uv sync

# Update .env with your Gemini API key
# Get your API key from: https://makersuite.google.com/app/apikey
notepad .env

# Run backend server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend running at: http://localhost:8000
API Docs: http://localhost:8000/docs

### Step 2: Setup Frontend

Open a NEW terminal:

```bash
# Navigate to frontend
cd forened

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend running at: http://localhost:3000

### Step 3: Test the System

1. Open browser: http://localhost:3000
2. Fill out support form:
   - Name: Test User
   - Email: test@example.com
   - Category: Technical
   - Message: This is a test message to verify the system is working correctly.
3. Click Submit
4. Note the Ticket ID
5. Click "Check Ticket Status"
6. Enter Ticket ID to view conversation

## ⚡ Quick Test Commands

### Test Backend Health
```bash
curl http://localhost:8000/health
```

### Test API Endpoint
```bash
curl -X POST http://localhost:8000/support/submit \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"Test User\",\"email\":\"test@example.com\",\"category\":\"General\",\"message\":\"This is a test message to verify the system.\"}"
```

### Run Playwright Tests
```bash
cd forened
npx playwright test
```

## 🔑 Get Gemini API Key

1. Go to: https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Create API key
4. Copy to backend/.env:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

## 🎨 Demo Features

### Feature 1: Web Form Submission
- Beautiful animated form
- Real-time validation
- Gradient buttons
- Instant ticket ID

### Feature 2: AI Response
- Gemini 2.0 Flash integration
- Response within 3 seconds
- Sentiment analysis
- Escalation detection

### Feature 3: Ticket Status
- Modal popup
- Conversation history
- Color-coded messages
- Sentiment indicators

### Feature 4: Responsive Design
- Works on mobile
- Tablet optimized
- Desktop layout

## 📊 Success Metrics

| Metric | Target | How to Verify |
|--------|--------|---------------|
| Response Time | < 3s | Watch for AI response |
| Form Validation | Works | Try invalid inputs |
| Ticket Creation | Instant | Check ticket ID display |
| Status Check | Works | Enter ticket ID |
| UI Animations | Smooth | Watch transitions |

## 🐛 Common Issues

### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.9+

# Reinstall dependencies
uv sync --upgrade
```

### Frontend won't start
```bash
# Clear cache
rm -rf node_modules .next
npm install
```

### API Connection Error
```bash
# Check backend is running
curl http://localhost:8000/health

# Check .env.local
cat forened/.env.local
# Should have: NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Database Error
- Check DATABASE_URL in backend/.env
- Verify internet connection (NeonDB is cloud-hosted)

## 🎯 Hackathon Demo Script

**Introduction** (30 seconds):
> "Welcome to Customer Success FTE - a 24/7 AI-powered multi-channel support system."

**Demo Step 1** (1 minute):
> "Let me submit a support request through our web form..."
> - Fill form
> - Submit
> - Show ticket ID

**Demo Step 2** (1 minute):
> "Our AI responds within 3 seconds using Gemini 2.0 Flash..."
> - Point out AI response
> - Show sentiment analysis

**Demo Step 3** (1 minute):
> "Customers can check their ticket status anytime..."
> - Click status button
> - Enter ticket ID
> - Show conversation history

**Demo Step 4** (30 seconds):
> "The system supports Email, WhatsApp, and Web forms..."
> - Mention multi-channel
> - Show database schema

**Conclusion** (30 seconds):
> "Built with FastAPI, Next.js, and Gemini AI. Response time under 3 seconds!"

## 📞 Support

For issues or questions:
1. Check README.md
2. Review API docs at /docs
3. Check Playwright tests for examples

---

**Happy Hacking! 🚀**
