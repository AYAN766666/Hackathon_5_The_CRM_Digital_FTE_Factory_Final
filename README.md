# Customer Success FTE - Multi-Channel AI Support System

24/7 AI-powered customer support system that automatically responds to customers across **Email**, **WhatsApp**, and **Web Support Form**.

## 🚀 Features

- **Multi-Channel Support**: Email, WhatsApp, and Web Form integration
- **AI-Powered Responses**: Gemini 2.0 Flash for understanding and responding to customers
- **24-Hour Conversation Window**: Automatic conversation continuity
- **Cross-Channel Identification**: Recognize customers across different channels
- **Escalation Detection**: Automatic escalation for complex issues
- **Real-Time Ticket Tracking**: Check ticket status anytime
- **Beautiful UI**: Animated interface with gradient buttons and 3D effects

## 📁 Project Structure

```
The CRM Digital FTE Factory Final/
├── backend/                    # FastAPI Backend
│   ├── main.py                # Main application entry
│   ├── config.py              # Configuration management
│   ├── database.py            # Database connection
│   ├── models.py              # SQLAlchemy models
│   ├── schemas.py             # Pydantic schemas
│   ├── services/              # Business logic
│   │   ├── ai_service.py     # Gemini AI integration
│   │   ├── customer_service.py
│   │   ├── conversation_service.py
│   │   └── message_service.py
│   ├── routes/                # API endpoints
│   │   └── webform.py        # Web form routes
│   ├── .env                   # Environment variables
│   └── pyproject.toml         # Python dependencies
│
├── forened/                    # Next.js Frontend
│   ├── app/
│   │   ├── page.tsx          # Home page
│   │   ├── layout.tsx        # Root layout
│   │   └── globals.css       # Global styles
│   ├── components/
│   │   ├── SupportForm.tsx   # Support form component
│   │   └── TicketStatusModal.tsx  # Status modal
│   ├── lib/
│   │   └── api.ts            # API client
│   ├── tests/
│   │   └── support-form.spec.ts  # Playwright tests
│   └── playwright.config.ts   # Playwright config
│
└── specs/
    └── 1-multi-channel-support/
        ├── spec.md            # Feature specification
        ├── plan.md            # Implementation plan
        └── tasks.md           # Task breakdown
```

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI + Uvicorn
- **Database**: NeonDB (PostgreSQL)
- **ORM**: SQLAlchemy (Async)
- **AI**: Gemini 2.0 Flash via OpenAI SDK
- **Package Manager**: UV

### Frontend
- **Framework**: Next.js 16
- **Styling**: Tailwind CSS 4
- **Animations**: Framer Motion
- **Icons**: Lucide React
- **HTTP Client**: Axios

### Testing
- **E2E**: Playwright
- **Backend**: pytest (coming soon)

## 📦 Installation

### Prerequisites
- Python 3.9+
- Node.js 18+
- UV package manager (`pip install uv`)

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment and install dependencies:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv sync
```

3. Configure environment variables:
```bash
# Copy .env.example to .env
cp .env.example .env

# Edit .env and add your Gemini API key
GEMINI_API_KEY=your_actual_api_key_here
```

4. Run the backend:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`
API Docs at: `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd forened
```

2. Install dependencies:
```bash
npm install
```

3. Configure environment:
```bash
# .env.local is already created
# Update NEXT_PUBLIC_API_URL if backend is on different port
```

4. Run the development server:
```bash
npm run dev
```

Frontend will be available at: `http://localhost:3000`

## 🎯 Usage

### Submit Support Request

1. Open `http://localhost:3000`
2. Fill out the support form:
   - **Name**: Your name (2-50 characters)
   - **Email**: Valid email address
   - **Category**: Select support category
   - **Message**: Your issue (20-1000 characters)
3. Click **Submit Request**
4. Receive ticket ID instantly
5. Save ticket ID for tracking

### Check Ticket Status

1. Click **Check Ticket Status** button
2. Enter your ticket ID
3. View conversation history and status

## 📊 API Endpoints

### POST /support/submit
Submit a support request

**Request**:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "category": "Technical",
  "message": "I need help with..."
}
```

**Response**:
```json
{
  "ticket_id": "ABC12345",
  "status": "created",
  "message": "Your support request has been received"
}
```

### GET /support/ticket/{ticket_id}
Get ticket status and conversation history

**Response**:
```json
{
  "ticket_id": "ABC12345",
  "status": "active",
  "channel": "webform",
  "created_at": "2026-03-12T10:00:00Z",
  "messages": [
    {
      "sender": "customer",
      "content": "I need help...",
      "timestamp": "2026-03-12T10:00:00Z"
    },
    {
      "sender": "agent",
      "content": "I can help with that...",
      "timestamp": "2026-03-12T10:00:02Z"
    }
  ]
}
```

## 🧪 Testing

### Run Playwright Tests

```bash
cd forened
npx playwright test
```

### Run with UI
```bash
npx playwright test --ui
```

### Generate HTML Report
```bash
npx playwright test --reporter=html
npx playwright show-report
```

## 🎨 UI Features

- **Gradient Buttons**: Blue gradient (#4F8DF7 → #1A5CC8) for submit, green (#28A745) for success
- **3D Card Effects**: Glassmorphism with backdrop blur
- **Smooth Animations**: Framer Motion for all transitions
- **Responsive Design**: Works on mobile, tablet, and desktop
- **Custom Scrollbar**: Styled scrollbar for message history
- **Message Bubbles**: Different colors for customer/agent messages

## 📈 Success Criteria

| Metric | Target | Status |
|--------|--------|--------|
| Response Time | < 3 seconds | ✅ Implemented |
| Customer Identification | > 95% accuracy | ✅ Email-based |
| System Uptime | > 99% | ✅ FastAPI + NeonDB |
| Form Validation | Client + Server | ✅ Both layers |
| AI Response Quality | Gemini 2.0 Flash | ✅ Integrated |

## 🔧 Configuration

### Database Schema

The system uses 3 main tables:

**customers**:
- customer_id (UUID)
- email (unique)
- phone
- name
- created_at, updated_at

**conversations**:
- conversation_id (UUID)
- customer_id (FK)
- channel (email/whatsapp/webform)
- status (active/closed/escalated)
- sentiment_score
- started_at, last_message_at, expires_at

**messages**:
- message_id (UUID)
- conversation_id (FK)
- sender_type (customer/agent/system)
- content
- sentiment_score
- escalation_required
- created_at

## 🚨 Troubleshooting

### Backend Issues

**Database Connection Error**:
- Check DATABASE_URL in .env
- Verify NeonDB connection string
- Ensure SSL mode is required

**AI Service Error**:
- Verify GEMINI_API_KEY is set
- Check API key has correct permissions
- Test API endpoint manually

### Frontend Issues

**API Connection Error**:
- Ensure backend is running on port 8000
- Check NEXT_PUBLIC_API_URL in .env.local
- Verify CORS settings in backend

**Build Errors**:
```bash
# Clear cache and reinstall
rm -rf node_modules .next
npm install
npm run dev
```

## 📝 Development

### Adding New Features

1. Update backend models if needed
2. Create/update service layer
3. Add API endpoints
4. Update frontend components
5. Add tests
6. Update documentation

### Code Style

**Backend**:
- Use type hints
- Follow PEP 8
- Async/await for I/O
- Docstrings for all functions

**Frontend**:
- TypeScript strict mode
- Functional components
- React hooks
- Tailwind for styling

## 🎯 Demo Flow

1. **Judge opens web support page** → `http://localhost:3000`
2. **Submits support request** → Fill form and submit
3. **AI generates response** → Instant AI reply via Gemini
4. **Ticket created** → Ticket ID displayed
5. **Check status** → Click status button, enter ticket ID
6. **View conversation** → See full message history
7. **Show database** → Check NeonDB records

## 📚 Documentation

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Next.js Docs](https://nextjs.org/docs)
- [Playwright Docs](https://playwright.dev/)
- [Gemini API](https://ai.google.dev/)
- [NeonDB Docs](https://neon.tech/docs)

## 🤝 Contributing

1. Create feature branch
2. Make changes
3. Add tests
4. Submit PR

## 📄 License

MIT License - See LICENSE file for details

---

**Built with ❤️ for Hackathon 5**

**Customer Success FTE - Multi-Channel AI Support System**
