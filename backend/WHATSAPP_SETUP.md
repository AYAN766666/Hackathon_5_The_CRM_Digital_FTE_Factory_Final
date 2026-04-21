# 📱 WhatsApp Integration Setup Guide

## ✅ What's Been Fixed

The WhatsApp integration has been upgraded to use a **persistent agent** that:

1. **Maintains a browser session** - No need to scan QR code every time
2. **Runs in the background** - Doesn't block the main application
3. **Saves login state** - First time scan, then always logged in
4. **Handles messages reliably** - Uses click-to-chat for guaranteed delivery

---

## 🚀 Quick Start

### Step 1: Install Playwright Browsers

```bash
cd backend
python -m playwright install chromium
```

### Step 2: Start the Backend

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Step 3: Initialize WhatsApp Agent (First Time Only)

**Option A: Use the startup script**
```bash
start-whatsapp-agent.bat
```

**Option B: Run manually**
```bash
python services\whatsapp_agent.py
```

### Step 4: Scan QR Code (First Time Only)

1. A browser window will open
2. You'll see a QR code on WhatsApp Web
3. Open WhatsApp on your phone
4. Go to: Settings → Linked Devices → Link a Device
5. Scan the QR code
6. ✅ You're now logged in!

**The session is saved**, so you only need to do this once.

---

## 🎯 How It Works

### Architecture

```
Web Form Submission
        ↓
Backend creates ticket
        ↓
Triggers WhatsApp Agent (async)
        ↓
Agent sends message via WhatsApp Web
        ↓
Customer receives WhatsApp message
```

### Session Persistence

- **First run**: Scan QR code → Session saved to `.whatsapp_session/`
- **Subsequent runs**: Auto-logged in → Ready to send immediately

---

## 📱 Testing WhatsApp

### Test via API

```bash
curl -X POST http://localhost:8000/whatsapp/send ^
  -H "Content-Type: application/json" ^
  -d "{\"phone_number\": \"923198130598\", \"message\": \"Hello from WhatsApp Agent!\"}"
```

### Test Ticket Notification

```bash
curl -X POST http://localhost:8000/support/submit ^
  -H "Content-Type: application/json" ^
  -d "{\"name\": \"Test User\", \"email\": \"test@example.com\", \"phone\": \"923198130598\", \"category\": \"Technical\", \"message\": \"Testing WhatsApp integration\"}"
```

### Check Agent Status

```bash
curl http://localhost:8000/whatsapp/status
```

---

## 🔧 Configuration

### Environment Variables (Optional)

Add to `backend/.env`:

```env
# WhatsApp Settings
WHATSAPP_SESSION_DIR=.whatsapp_session
WHATSAPP_TIMEOUT=60
```

### Phone Number Format

Phone numbers must include country code **without** the `+`:

- ✅ `923198130598` (correct)
- ✅ `14155552671` (correct)
- ❌ `+923198130598` (remove the +)
- ❌ `03198130598` (missing country code)

---

## 🎬 Demo Flow

### For Hackathon Demo:

1. **Start backend**: `uvicorn main:app --reload`
2. **Ensure WhatsApp is logged in**: Run agent once before demo
3. **Open web form**: `http://localhost:3000`
4. **Fill form with phone number**: 
   - Name: Judge Name
   - Email: judge@example.com
   - Phone: 923198130598
   - Category: Technical
   - Message: Your issue here
5. **Submit**: Ticket created + WhatsApp sent instantly
6. **Show phone**: Judge receives WhatsApp message with ticket ID

---

## ⚠️ Troubleshooting

### QR Code Keeps Appearing

**Problem**: Session not saving

**Solution**:
```bash
# Close all browser windows
# Delete session folder
rmdir /s /q .whatsapp_session

# Restart agent
python services\whatsapp_agent.py

# Scan QR code again and keep browser open for 10 seconds
```

### Browser Won't Open

**Problem**: Playwright browser not launching

**Solution**:
```bash
# Reinstall Playwright browsers
python -m playwright install chromium --force

# Check if Chromium is installed
python -m playwright install chromium --dry-run
```

### Message Not Sending

**Problem**: Click-to-chat fails

**Solution**:
1. Check internet connection
2. Ensure phone number format is correct
3. Verify WhatsApp Web is logged in
4. Check browser console for errors

### Agent Not Starting

**Problem**: Import errors or crashes

**Solution**:
```bash
# Ensure dependencies are installed
pip install playwright

# Or using UV
uv sync

# Install Playwright browsers
python -m playwright install chromium
```

---

## 📊 API Endpoints

### POST /whatsapp/send
Send a WhatsApp message

**Request**:
```json
{
  "phone_number": "923198130598",
  "message": "Hello from API!"
}
```

**Response**:
```json
{
  "status": "sent",
  "message": "WhatsApp message sent successfully"
}
```

---

### POST /whatsapp/send-ticket
Send ticket notification (async)

**Request**:
```json
{
  "phone_number": "923198130598",
  "ticket_id": "ABC12345",
  "customer_name": "John Doe"
}
```

**Response**:
```json
{
  "status": "queued",
  "message": "WhatsApp notification queued for sending"
}
```

---

### GET /whatsapp/status
Check agent status

**Response**:
```json
{
  "status": "connected",
  "is_running": true,
  "queue_size": 0
}
```

---

### POST /whatsapp/initialize
Manually initialize agent

**Response**:
```json
{
  "status": "initialized",
  "message": "WhatsApp agent initialized successfully"
}
```

---

## 💡 Tips for Demo

1. **Pre-login before demo**: Run agent once, scan QR, close it
2. **Keep backend running**: Agent auto-starts with backend
3. **Use real phone number**: Test with your actual WhatsApp
4. **Show both channels**: Demonstrate email + WhatsApp together
5. **Explain persistence**: Session saved, no repeated QR scans

---

## 🏆 Features

✅ Persistent browser session
✅ QR code scan once, saved forever
✅ Async message sending (non-blocking)
✅ Click-to-chat fallback
✅ Message queue for reliability
✅ Auto-reconnect on failure
✅ Session stored locally
✅ Works with any WhatsApp number

---

## 📝 Session Location

Browser session is stored in:
```
backend/.whatsapp_session/
```

This folder contains:
- Browser cookies
- WhatsApp login tokens
- Local storage data

**Don't delete this folder** unless you want to re-scan QR code.

---

## 🎉 Ready for Hackathon!

WhatsApp integration is now:
- ✅ Reliable
- ✅ Fast
- ✅ Persistent
- ✅ Demo-ready

**Good luck!** 🚀
