# Quickstart Guide: Multi-Channel AI Support System

## 1. Prerequisites
- Node.js 18+ for frontend
- Python 3.9+ for backend
- Docker and Docker Compose for local Kafka
- Access to Gmail API and Twilio WhatsApp Sandbox

## 2. Setup Steps
1. Clone the repository
2. Install backend dependencies: `pip install fastapi uvicorn asyncpg aiokafka python-multipart`
3. Install frontend dependencies: `npm install next react react-dom`
4. Set up environment variables for API keys
5. Start Kafka locally: `docker-compose up kafka`
6. Initialize database: `python -m database init`
7. Start backend: `uvicorn main:app --reload`
8. Start frontend: `npm run dev`

## 3. Environment Variables
```
GEMINI_API_KEY=your_gemini_api_key
DATABASE_URL=postgresql://user:pass@localhost/dbname
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
GMAIL_WEBHOOK_SECRET=your_secret
TWILIO_AUTH_TOKEN=your_token
```

## 4. Running Tests
- Unit tests: `pytest`
- E2E tests: `playwright test`
- Load tests: `locust -f locustfile.py`

## 5. Development Commands
- Format code: `black . && isort .`
- Run linter: `flake8 .`
- Check types: `mypy .`