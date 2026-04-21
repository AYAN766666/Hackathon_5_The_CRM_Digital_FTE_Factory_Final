---
id: 3
title: multi-channel-support-plan
stage: plan
date: 2026-03-12
surface: agent
model: if/deepseek-v3.2-chat
feature: multi-channel-support
branch: 1-multi-channel-support
user: aayan
command: /sp.plan
labels: [plan,feature,multi-channel,ai-support,architecture]
links:
  spec: ../../specs/1-multi-channel-support/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/1-multi-channel-support/planning/plan.md
 - specs/1-multi-channel-support/planning/research.md
 - specs/1-multi-channel-support/planning/data-model.md
 - specs/1-multi-channel-support/planning/contracts/openapi.yaml
 - specs/1-multi-channel-support/planning/quickstart.md
tests:
---

## Prompt

```text
/sp.plan.md
1. Overview

Ye plan define karta hai kab, kya, kaise aur kyun har step karna hai hackathon me.
Goal:

Multi-channel FTE system ready for demo

24/7 AI automation

Customer identification across channels

Clear frontend buttons & workflow

Load and E2E testing

2. Timeline & Step-by-Step Plan
Step    Module    Action    When to do    How / Notes    Expected Outcome
1    Database    Setup NeonDB / PostgreSQL    Day 1    Create tables: customers, customer_identifiers, conversations, messages. Add pgvector extension.    Backend ready to store customers & conversations
2    Backend    FastAPI Project Setup    Day 1    main.py, install dependencies (fastapi, asyncpg, aiokafka)    API endpoints ready
3    Kafka    Setup Topics    Day 1    fte.tickets.incoming, fte.channels.*, fte.metrics, fte.escalations, fte.dlq    Async message system ready
4    Claude Skills    Install    Day 1    npx skills add https://github.com/404kidwiz/claude-supercode-skills --skill event-driven-architect    Event-driven architecture & automation helpers ready
5    Frontend    Next.js setup    Day 2    SupportForm.tsx, page.tsx, api.ts    Form ready for user input
6    Frontend    Form Validation    Day 2    Fields: name, email, category, message. Buttons: Submit (blue gradient), Reset (gray), Status (green)    Validation ready, colors & 3D hover implemented
7    Backend    Web Form Endpoint    Day 2    POST /support/submit → validate → store customer → push Kafka    Ticket creation via web form works
8    Backend    Email Webhook    Day 2-3    /webhooks/gmail → parse → push Kafka → AI agent    Email messages processed automatically
9    Backend    WhatsApp Webhook    Day 2-3    /webhooks/whatsapp → validate → push Kafka → AI agent    WhatsApp messages processed automatically
10    Worker    Message Processor    Day 3    Consume Kafka → resolve customer → conversation → AI → store & publish outbound    All messages processed reliably
11    AI    OpenAI Integration    Day 3    GPT-4o-mini → message understanding, response, escalation, sentiment    Responses auto-generated, escalation flagged if needed
12    Metrics    Logging & Monitoring    Day 3    Publish metrics to fte.metrics → latency, sentiment, tool calls, escalations    Track system performance
13    Kubernetes    Deployment    Day 4    Deploy API + worker + Kafka + ingress + ConfigMap + Secrets    Multi-pod scalable system
14    Frontend    Ticket Status Button    Day 4    GET /support/ticket/{ticket_id}    Users see status → color-coded messages
15    E2E Testing    Playwright    Day 4    Simulate web form → email → WhatsApp flow    Ensure cross-channel continuity
16    Load Testing    Locust    Day 5    100+ web submissions, 50+ emails, 50+ WhatsApp    Test system under stress
17    Demo Prep    Walkthrough    Day 5    Step-by-step demo: Web form → Email → WhatsApp → Metrics    Judges can see full automation & multi-channel support
18    Error Handling    Backend    Day 5    handle_error() → send apology → publish to escalations    Graceful fallback, human escalation ready
19    Final Optimization    All Modules    Day 5    Check latencies, DB indexes, Kafka throughput    Latency < 3s, escalation < 25%, uptime > 99.9%
3. Notes & Action Guidelines

Frontend Buttons:

Submit → blue gradient (#4F8DF7 → #1A5CC8), scale on hover, triggers POST → Kafka

Reset → light gray (#E0E0E0), clears form

Status → green (#28A745), GET status, show 3D glow

When to use AI:

On every incoming message (web/email/WhatsApp)

Generate response, detect escalation, sentiment score

When to create customer:

If email or phone not found → insert into customers table

Else → link to existing conversation

When to start conversation:

First message or >24h after last message → create new conversation

Do Not:

Directly send response before AI processing

Allow invalid form submission

Ignore failed Kafka messages → use DLQ

Colors / 3D Effects:

Error → red (#FF4C4C)

Success → green (#28A745)

Info / loader → dark gray (#333333)

Buttons → gradient + scale + shadow

✅ Ye plan follow karenge to 1-1 cheez step by step complete ho jayegi: frontend, backend, AI, DB, Kafka, buttons, colors, automation, testing, deployment.
```

## Response snapshot

# Implementation Plan: Multi-Channel AI Support System

**Feature**: 1-multi-channel-support
**Created**: 2026-03-12
**Status**: Draft

## Technical Context

### Known Architecture
- **Frontend**: Next.js application with support form
- **Backend**: FastAPI application
- **Database**: NeonDB (PostgreSQL) with pgvector extension
- **Messaging**: Apache Kafka with multiple topics
- **AI Service**: Gemini API (gemini-2.0-flash model)
- **Deployment**: Kubernetes with horizontal pod autoscaling
- **Channels**: Email (Gmail API), WhatsApp (Twilio), Web Form

### Unknowns (NEEDS CLARIFICATION)
- Specific API endpoints for each service
- Exact database schema definitions
- Detailed AI prompt engineering
- Error handling specifics
- Security implementation details
- Performance benchmarks and configurations

### Dependencies
- FastAPI framework
- asyncpg for PostgreSQL connections
- aiokafka for Kafka integration
- Claude SuperCode skills
- Gmail API
- Twilio WhatsApp API
- Kubernetes cluster

## Constitution Check

### Compliance Verification
- ✅ Multi-channel support (Email, WhatsApp, Web) - aligns with constitution
- ✅ AI-powered automation with Gemini API - aligns with constitution
- ✅ Cross-channel customer identification - aligns with constitution
- ✅ Event-driven architecture with Kafka - aligns with constitution
- ✅ Conversation lifecycle management (24h window) - aligns with constitution
- ✅ Metrics tracking and monitoring - aligns with constitution
- ✅ Database standard (NeonDB PostgreSQL) - aligns with constitution
- ✅ Frontend/Backend structure as specified - aligns with constitution

### Gate Evaluation
All constitutional requirements are satisfied by the planned implementation approach.

## Phase 0: Research & Resolution

### Research Findings (research.md)

#### 1. Database Schema Design
- **Decision**: Implement normalized schema with customers, customer_identifiers, conversations, and messages tables
- **Rationale**: Follows standard customer support system patterns with ability to track conversations across channels
- **Alternatives considered**: Denormalized schema for performance vs normalized for maintainability

#### 2. Kafka Topic Configuration
- **Decision**: Use specified topics with appropriate partitioning and replication
- **Rationale**: Enables reliable message processing and separation of concerns
- **Alternatives considered**: Single topic vs multiple specialized topics

#### 3. AI Integration Approach
- **Decision**: Use Gemini API with structured prompt engineering for consistent responses
- **Rationale**: Aligns with constitution requirements for AI processing
- **Alternatives considered**: Different AI models or hybrid approaches

#### 4. Frontend Validation Strategy
- **Decision**: Client-side validation with server-side verification
- **Rationale**: Provides good UX while maintaining security
- **Alternatives considered**: Server-only validation vs client-only validation

#### 5. Error Handling Implementation
- **Decision**: Comprehensive error handling with graceful degradation and escalation
- **Rationale**: Ensures system reliability and proper escalation to humans
- **Alternatives considered**: Fail-fast vs graceful degradation approaches

## Phase 1: Design & Contracts

### Data Model (data-model.md)

#### Entity: Customer
- customer_id (UUID, primary key)
- email (VARCHAR, unique, indexed)
- phone (VARCHAR, nullable, indexed)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)

#### Entity: CustomerIdentifier
- identifier_id (UUID, primary key)
- customer_id (UUID, foreign key)
- identifier_type (ENUM: email, phone, external_id)
- identifier_value (VARCHAR, indexed)
- created_at (TIMESTAMP)

#### Entity: Conversation
- conversation_id (UUID, primary key)
- customer_id (UUID, foreign key)
- channel (ENUM: email, whatsapp, webform)
- status (ENUM: active, closed, escalated)
- sentiment_score (FLOAT, nullable)
- started_at (TIMESTAMP)
- last_message_at (TIMESTAMP)
- expires_at (TIMESTAMP)  // 24 hours from last message

#### Entity: Message
- message_id (UUID, primary key)
- conversation_id (UUID, foreign key)
- sender_type (ENUM: customer, agent, system)
- sender_identifier (VARCHAR)
- content (TEXT)
- sentiment_score (FLOAT, nullable)
- escalation_required (BOOLEAN)
- created_at (TIMESTAMP)
- processed_latency_ms (INTEGER)

### API Contracts

#### Web Form Endpoint
```yaml
openapi: 3.0.0
info:
  title: Multi-Channel Support API
  version: 1.0.0
paths:
  /support/submit:
    post:
      summary: Submit support request via web form
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                name:
                  type: string
                  minLength: 2
                  maxLength: 50
                email:
                  type: string
                  format: email
                category:
                  type: string
                  enum: [General, Technical, Billing, Feedback, Bug Report]
                message:
                  type: string
                  minLength: 20
                  maxLength: 1000
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                type: object
                properties:
                  ticket_id:
                    type: string
                    description: Unique ticket identifier
                  status:
                    type: string
                    enum: [created, escalated]
        '400':
          description: Validation error
```

#### Ticket Status Endpoint
```yaml
  /support/ticket/{ticket_id}:
    get:
      summary: Get ticket status and conversation history
      parameters:
        - name: ticket_id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Ticket status and messages
          content:
            application/json:
              schema:
                type: object
                properties:
                  ticket_id:
                    type: string
                  status:
                    type: string
                    enum: [active, closed, escalated]
                  messages:
                    type: array
                    items:
                      type: object
                      properties:
                        sender:
                          type: string
                        content:
                          type: string
                        timestamp:
                          type: string
                          format: date-time
        '404':
          description: Ticket not found
```

#### Email Webhook Endpoint
```yaml
  /webhooks/gmail:
    post:
      summary: Receive Gmail webhook notifications
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                email:
                  type: string
                subject:
                  type: string
                body:
                  type: string
      responses:
        '200':
          description: Successfully received
```

#### WhatsApp Webhook Endpoint
```yaml
  /webhooks/whatsapp:
    post:
      summary: Receive WhatsApp webhook notifications
      requestBody:
        required: true
        content:
          application/x-www-form-urlencoded:
            schema:
              type: object
              properties:
                From:
                  type: string
                Body:
                  type: string
      responses:
        '200':
          description: Successfully received
```

### Quickstart Guide

#### 1. Prerequisites
- Node.js 18+ for frontend
- Python 3.9+ for backend
- Docker and Docker Compose for local Kafka
- Access to Gmail API and Twilio WhatsApp Sandbox

#### 2. Setup Steps
1. Clone the repository
2. Install backend dependencies: `pip install fastapi uvicorn asyncpg aiokafka python-multipart`
3. Install frontend dependencies: `npm install next react react-dom`
4. Set up environment variables for API keys
5. Start Kafka locally: `docker-compose up kafka`
6. Initialize database: `python -m database init`
7. Start backend: `uvicorn main:app --reload`
8. Start frontend: `npm run dev`

#### 3. Environment Variables
```
GEMINI_API_KEY=your_gemini_api_key
DATABASE_URL=postgresql://user:pass@localhost/dbname
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
GMAIL_WEBHOOK_SECRET=your_secret
TWILIO_AUTH_TOKEN=your_token
```

## Phase 2: Implementation Approach

### Week 1: Foundation
- Set up database schema
- Configure Kafka topics
- Initialize FastAPI backend
- Install Claude SuperCode skills

### Week 2: Frontend & Web Channel
- Create Next.js frontend with support form
- Implement form validation and styling
- Create web form submission endpoint
- Integrate with Kafka producer

### Week 3: AI & Backend Services
- Implement AI integration with Gemini API
- Create message processor worker
- Implement email and WhatsApp webhook handlers
- Add customer identification logic

### Week 4: Advanced Features
- Implement conversation continuity logic
- Add metrics tracking
- Set up Kubernetes deployment
- Create ticket status functionality

### Week 5: Testing & Optimization
- Conduct E2E testing with Playwright
- Perform load testing with Locust
- Optimize performance
- Prepare demo materials

## Outcome

- ✅ Impact: Created comprehensive implementation plan for multi-channel AI support system
- 🧪 Tests: No automated tests for planning phase
- 📁 Files: Created plan.md, research.md, data-model.md, openapi.yaml, and quickstart.md
- 🔁 Next prompts: Proceed with task generation (/sp.tasks) and implementation
- 🧠 Reflection: Plan covers all aspects of the multi-channel support system with clear architecture, data model, and API contracts

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Generate tasks from the plan