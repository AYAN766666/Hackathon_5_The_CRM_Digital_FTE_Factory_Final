---
id: 1
title: constitution-update-customer-success-fte
stage: constitution
date: 2026-03-12
surface: agent
model: if/deepseek-v3.2-chat
feature: customer-success-fte
branch: main
user: aayan
command: /sp.constitution
labels: [constitution,architecture,setup]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
---

## Prompt

```text
# /sp.constitution.md

## 1. Project Name

**Customer Success FTE – Multi-Channel AI Support System**

Goal:
Build a **24/7 AI powered customer support system** that can receive and respond to users through:

* Email
* WhatsApp
* Web Support Form

System must store all conversations, identify customers across channels, and auto-respond using AI.

---

# 2. Core Technologies (Complete Stack)

## AI Layer
pakage openai ka use hoga or confiragtion gemini ki go example
async def main():
    api_key = os.getenv("GEMINI_API_KEY")

    external_client = AsyncOpenAI(
        api_key=api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    model = OpenAIChatCompletionsModel(
        model = "gemini-2.0-flash",
        openai_client=external_client
    )

    run_config = RunConfig(
         model=model,
         model_provider=external_client,
         tracing_disabled=True


* **Gemini API**
* Model: `gemini-flas.202` or `gemini-flash2.0`

Purpose:

* Understand customer message
* Generate response
* Detect escalation cases
* Extract structured data

Also used for:

* message classification
* sentiment scoring
* tool calling

---

## Backend

Framework:

* **FastAPI**

Purpose:

* API endpoints
* webhooks
* conversation management
* ticket creation
* AI agent calling

Server command:

```bash
uvicorn main:app --reload
```

---

## Database

Database:

**NeonDB (PostgreSQL)**

Purpose:

* store customers
* store conversations
* store messages
* store metrics

Tables:

* customers
* customer_identifiers
* conversations
* messages

Extensions:

```
pgvector
```

Used for embeddings if knowledge search is implemented.

---

# 3. Event System

Messaging system:

**Apache Kafka**

Purpose:

* async message processing
* channel separation
* reliability
* scalability

Topics:

```
fte.tickets.incoming
fte.channels.email.inbound
fte.channels.whatsapp.inbound
fte.channels.webform.inbound
fte.channels.email.outbound
fte.channels.whatsapp.outbound
fte.metrics
fte.escalations
fte.dlq
```

---

# 4. Channels (User Communication)

## Email

API:

Gmail API

Flow:

```
Customer Email
↓
Gmail Webhook
↓
FastAPI
↓
Kafka
↓
AI Agent
↓
Email Response
```

---

## WhatsApp

Integration:

Twilio WhatsApp Sandbox

Flow:

```
Customer WhatsApp
↓
Twilio Webhook
↓
FastAPI
↓
Kafka
↓
AI Agent
↓
WhatsApp Response
```

---

## Web Support Form

Frontend:

Next.js

Form fields:

* Name
* Email
* Category
* Message

Submission endpoint:

```
POST /support/submit
```

Ticket status endpoint:

```
GET /support/ticket/{ticket_id}
```

---

# 5. AI Processing

AI agent responsibilities:

1 Understand message
2 Identify customer intent
3 Retrieve conversation context
4 Generate helpful response
5 Decide if escalation required

Example prompt:

```
You are a customer support assistant.

Understand the customer message.
Provide a helpful answer.

If the problem cannot be solved automatically
mark escalation_required = true.
```

---

# 6. Customer Identification

System must identify users across channels.

Matching priority:

1 email
2 phone number
3 other identifiers

Example:

Customer sends email → customer created.

Later same person messages on WhatsApp.

System must link both identities to the same customer record.

---

# 7. Conversation Rules

Conversation lifecycle:

Active window:

```
24 hours
```

If message arrives after 24 hours:

Create new conversation.

Conversation table stores:

* customer_id
* channel
* sentiment_score
* status

---

# 8. Metrics Tracking

Every message stores metrics:

* latency_ms
* sentiment_score
* tool_calls
* escalation_required

Metrics published to:

```
fte.metrics
```

---

# 9. Skills Installation

Install Claude SuperCode skills:

```bash
npx skills add https://github.com/404kidwiz/claude-supercode-skills --skill event-driven-architect
```

Optional skills:

```
web-form-handler
channel-integration
```

Purpose:

* event driven architecture
* channel processing
* automation helpers

---

# 10. Backend Folder Structure

```
backend/

main.py
database.py
models.py
schemas.py

routes/
email.py
whatsapp.py
webform.py

workers/
message_processor.py

services/
ai_agent.py
customer_service.py
conversation_service.py
```

---

# 11. Frontend Folder Structure

```
frontend/

app/
support/
page.tsx

components/
SupportForm.tsx

lib/
api.ts
```

---

# 12. Kubernetes Deployment

Deployment components:

* API Deployment
* Worker Deployment
* Kafka
* Ingress
* ConfigMap
* Secrets

Namespace:

```
customer-success-fte
```

Pods:

```
api-pod
worker-pod
```

Scaling:

Horizontal Pod Autoscaler enabled.

---

# 13. Testing

Testing frameworks:

Backend:

pytest

Frontend:

Playwright

Load testing:

Locust

Test scenarios:

* 100+ web submissions
* 50+ email messages
* 50+ WhatsApp messages
* cross channel customers

---

# 14. Hackathon Demo Flow

Demo scenario:

1 Customer submits web form
2 System creates ticket
3 AI generates response
4 Email reply sent
5 User replies on WhatsApp
6 System identifies same customer
7 Conversation continues

Judges see:

* multi channel su
```

## Response snapshot

# Customer Success FTE – Multi-Channel AI Support System Constitution

## Core Principles

### Customer Success FTE – Multi-Channel AI Support System
Multi-channel AI-powered customer support system that receives and responds to users through Email, WhatsApp, and Web Support Form. System must store all conversations, identify customers across channels, and auto-respond using AI.

### AI-Powered Customer Support
Uses Gemini API with gemini-2.0-flash or gemini-flash2.0 model for understanding customer messages, generating responses, detecting escalation cases, extracting structured data, message classification, sentiment scoring, and tool calling.

### Event-Driven Architecture with Apache Kafka
Uses Apache Kafka for asynchronous message processing, channel separation, reliability, and scalability. Key topics include fte.tickets.incoming, fte.channels.email.inbound, fte.channels.whatsapp.inbound, fte.channels.webform.inbound, fte.channels.email.outbound, fte.channels.whatsapp.outbound, fte.metrics, fte.escalations, and fte.dlq.

### Cross-Channel Customer Identification
System must identify users across channels with matching priority: email, phone number, other identifiers. Customers sending emails should be linked to subsequent WhatsApp messages from the same person.

### Conversation Lifecycle Management
Conversations have a 24-hour active window. If a message arrives after 24 hours, a new conversation is created. Conversation table stores customer_id, channel, sentiment_score, and status.

### Backend Framework Standardization
Uses FastAPI for API endpoints, webhooks, conversation management, ticket creation, and AI agent calling. Server command: uvicorn main:app --reload.

## Technology Stack

### Database Standard
Uses NeonDB (PostgreSQL) to store customers, conversations, messages, and metrics. Tables include customers, customer_identifiers, conversations, and messages. pgvector extension for embeddings if knowledge search is implemented.

### Channel Integration Protocols
- Email: Gmail API with webhook flow to FastAPI → Kafka → AI Agent → Email Response
- WhatsApp: Twilio WhatsApp Sandbox with webhook flow to FastAPI → Kafka → AI Agent → WhatsApp Response
- Web Support Form: Next.js frontend with Name, Email, Category, Message fields

## Development Standards

### AI Processing Responsibilities
AI agent responsibilities include: understanding message, identifying customer intent, retrieving conversation context, generating helpful response, and deciding if escalation required. Example prompt: "You are a customer support assistant. Understand the customer message. Provide a helpful answer. If the problem cannot be solved automatically mark escalation_required = true."

### Metrics and Monitoring
Every message stores metrics: latency_ms, sentiment_score, tool_calls, escalation_required. Metrics published to fte.metrics topic for monitoring and analysis.

### Skills and Automation
Install Claude SuperCode skills for event-driven architecture, channel processing, and automation helpers. Command: npx skills add https://github.com/404kidwiz/claude-supercode-skills --skill event-driven-architect

## System Architecture

### Folder Structure Standards
Backend folder structure includes main.py, database.py, models.py, schemas.py, routes/email.py, whatsapp.py, webform.py, workers/message_processor.py, and services/ai_agent.py, customer_service.py, conversation_service.py.
Frontend folder structure includes app/support/page.tsx, components/SupportForm.tsx, and lib/api.ts.

### Deployment Strategy
Kubernetes deployment with API Deployment, Worker Deployment, Kafka, Ingress, ConfigMap, and Secrets in customer-success-fte namespace. Horizontal Pod Autoscaler enabled for scaling.

### Testing Frameworks
Backend: pytest; Frontend: Playwright; Load testing: Locust. Test scenarios include 100+ web submissions, 50+ email messages, 50+ WhatsApp messages, and cross-channel customers.

## Governance

This constitution establishes the foundational principles for the Customer Success FTE – Multi-Channel AI Support System. All development, testing, and deployment activities must comply with these principles. Changes to these principles require explicit approval and documentation of the impact on existing systems. All team members must adhere to the technology stack, architecture patterns, and development standards outlined herein.

**Version**: 1.1.0 | **Ratified**: 2026-03-12 | **Last Amended**: 2026-03-12

## Outcome

- ✅ Impact: Updated project constitution with comprehensive architecture for multi-channel AI support system
- 🧪 Tests: No tests needed for constitution update
- 📁 Files: Modified .specify/memory/constitution.md
- 🔁 Next prompts: Proceed with feature specification and implementation planning
- 🧠 Reflection: Constitution now properly defines the core principles and architecture for the customer success system

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin feature specification based on constitution