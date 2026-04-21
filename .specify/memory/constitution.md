<!-- SYNC IMPACT REPORT:
Version change: 1.0.0 → 1.1.0
Modified principles: [PRINCIPLE_1_NAME] → Customer Success FTE – Multi-Channel AI Support System
Added sections: Core Technologies, Event System, Channel Integration, AI Processing, Customer Identification, Conversation Rules, Metrics Tracking, Skills Installation, Backend/Frontend Structure, Kubernetes Deployment, Testing, Demo Flow
Removed sections: None
Templates requiring updates: ✅ Updated
Follow-up TODOs: None
-->
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