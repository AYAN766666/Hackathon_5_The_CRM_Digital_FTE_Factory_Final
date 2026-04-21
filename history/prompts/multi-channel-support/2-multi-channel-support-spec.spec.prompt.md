---
id: 2
title: multi-channel-support-spec
stage: spec
date: 2026-03-12
surface: agent
model: if/deepseek-v3.2-chat
feature: multi-channel-support
branch: 1-multi-channel-support
user: aayan
command: /sp.specify
labels: [spec,feature,multi-channel,ai-support]
links:
  spec: ./specs/1-multi-channel-support/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/1-multi-channel-support/spec.md
 - specs/1-multi-channel-support/checklists/requirements.md
tests:
---

## Prompt

```text
## Email Handling

1. Gmail webhook receives new email
2. FastAPI endpoint `/webhooks/gmail` parses email
3. Push message to Kafka topic `fte.tickets.incoming`
4. Message processor picks event
5. AI agent:
   - Classifies intent
   - Checks previous conversation (last 24h)
   - Generates response
6. If escalated:
   - Publish to `fte.escalations`
7. Otherwise:
   - Send reply via Gmail API 1. Overview

Ye file define karti hai har module ka kaam, trigger, frontend behavior, button actions, colors, AI responses aur automation flow.

Goal:

Multi-channel support (Email, WhatsApp, Web)

24/7 AI automation

Customer identification & conversation continuity

Visual feedback on frontend (buttons, colors, 3D effects)

2. Web Support Form (Frontend)

Framework: Next.js
File: frontend/app/support/page.tsx
Component: SupportForm.tsx

Form Fields:
Field    Type    Placeholder    Validation
Name    text    "Your Name"    min 2 char, max 50
Email    email    "your@email.com
"    valid email format
Category    select    "Select Category"    options: General, Technical, Billing, Feedback, Bug Report
Message    textarea    "Describe your issue"    min 20 char, max 1000
Buttons:
Button    Color    Action    3D Effect
Submit    Gradient Blue (#4F8DF7 → #1A5CC8)    On click, validate fields → POST /support/submit → Disable button → Show loader    Shadow and hover pop effect (scale 1.05)
Reset    Light Gray (#E0E0E0)    Clears all fields    Flat, subtle shadow
Status    Green (#28A745)    Opens ticket status modal → GET /support/ticket/{ticket_id}    Rounded 3D button with hover glow
Form Submission Flow:

User fills form → clicks Submit

Client validates fields → highlights missing/invalid fields in red (#FF4C4C)

On success:

POST request to FastAPI /support/submit

Show loader with text: "Submitting..." in dark gray (#333333)

Backend receives request → creates customer (if not exists)

Backend pushes message to Kafka topic: fte.tickets.incoming

AI agent processes → generates response → stores message

Frontend shows success message: "Ticket created! ID: {ticket_id}" in green (#28A745)

3. Email Handling (Backend)

Endpoint: /webhooks/gmail
Trigger: Gmail Pub/Sub webhook

Flow:

Gmail sends notification → FastAPI endpoint receives JSON

Parse email → extract subject, body, customer_email

Push message to Kafka topic: fte.tickets.incoming

AI agent workflow:

Identify customer by email

Retrieve last 24h conversation

Generate response

Detect escalation if problem unsolvable automatically

Response:

If escalated → Publish to fte.escalations

Else → Send reply via Gmail API

Log metrics → fte.metrics

4. WhatsApp Handling (Backend)

Endpoint: /webhooks/whatsapp
Integration: Twilio Sandbox

Flow:

Twilio webhook → FastAPI receives form data

Validate signature

Push message to Kafka topic: fte.tickets.incoming

AI agent:

Identify customer by phone

Retrieve conversation context

Generate reply

Decide escalation

Response:

Send message via Twilio WhatsApp API

Log metrics to fte.metrics

5. Kafka Event Processing

Purpose: Async message processing for all channels

Topic    Purpose
fte.tickets.incoming    Unified queue for AI agent processing
fte.channels.email.outbound    Email responses
fte.channels.whatsapp.outbound    WhatsApp responses
fte.metrics    Performance monitoring
fte.escalations    Messages requiring human attention
fte.dlq    Failed message processing
Worker Flow (message_processor.py):

Consume message from Kafka

Resolve customer (email → phone → identifiers)

Get or create conversation (check last 24h)

Call AI agent:

Understand intent

Retrieve conversation context

Generate response

Decide escalation

Store message & metrics

Publish outbound response to respective Kafka topic

If error → call handle_error() → send apology → publish to fte.escalations

6. AI Agent / OpenAI

Model: gpt-4o-mini
Tasks:

Message understanding

Response generation

Escalation detection

Sentiment scoring

Tool calls

Example Prompt:
You are a customer support assistant.
Understand the message.
Generate a helpful response.
If the problem cannot be solved automatically, mark escalation_required = true.
7. Customer Identification Rules

Email → primary

Phone → secondary (WhatsApp)

Other identifiers → optional

Example:

Customer sends email → new customer

Later messages WhatsApp → system links both to same customer record

8. Conversation Rules

Active conversation window → 24h

New conversation created if outside 24h

Conversation table stores:

customer_id

channel

sentiment_score

status

9. Metrics Tracking

Every processed message logs:

latency_ms

sentiment_score

tool_calls_count

escalation_required

10. Buttons / Automation in Frontend
UI Element    Trigger    Backend Action    AI Action    Color / 3D
Submit    Click    POST /support/submit    Push to Kafka → AI → Response    Blue Gradient (#4F8DF7 → #1A5CC8), shadow 3D hover
Status    Click    GET /support/ticket/{ticket_id}    Fetch messages    Green (#28A745), hover glow
Reset    Click    Clear form    None    Light Gray (#E0E0E0), flat button
11. Colors / Visual Guide

Errors → Red (#FF4C4C)

Success → Green (#28A745)

Info / Loader → Dark Gray (#333333)

Buttons → Gradient / 3D hover

3D effect → transform: scale(1.05) on hover, shadow below

12. Testing & Load
Type    Tool    Scenario
Unit    pytest    Backend endpoints
E2E    Playwright    Web form & cross-channel
Load    Locust    100+ web submissions, 50+ emails, 50+ WhatsApp messages
Metrics    Manual / script    Latency < 3s, Escalation < 25%, Customer ID > 95%
13. Hackathon Demo Flow

Submit web form → Tick
```

## Response snapshot

# Feature Specification: Multi-Channel AI Support System

**Feature Branch**: `1-multi-channel-support`
**Created**: 2026-03-12
**Status**: Draft
**Input**: User description: "Multi-channel AI support system for Email, WhatsApp, and Web forms with 24/7 automation, customer identification, and conversation continuity."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Submit Support Request via Web Form (Priority: P1)

A customer visits the website and needs help with a product or service. They fill out the support form with their name, email, category, and message. Upon submission, they receive immediate feedback that their request has been received and is being processed by the AI support system. The customer receives a ticket ID for tracking purposes.

**Why this priority**: This is the primary entry point for customer support and enables the entire system to function. Without this basic capability, the multi-channel support system cannot operate.

**Independent Test**: Can be fully tested by filling out the web form and verifying that a ticket is created with proper validation, showing the ticket ID to the user, and delivering immediate value by capturing customer requests.

**Acceptance Scenarios**:

1. **Given** a customer on the support page, **When** they submit a valid form with all required fields, **Then** a support ticket is created and they receive a ticket ID
2. **Given** a customer on the support page, **When** they submit an invalid form with missing or incorrect data, **Then** they receive clear error messages highlighting the problematic fields

---

### User Story 2 - Receive AI Response via Email (Priority: P1)

A customer sends an email to the support address and expects a timely response. The system receives the email, processes it with the AI agent, and sends back a helpful response. If the AI cannot resolve the issue, it escalates to human support.

**Why this priority**: Email is a primary communication channel for business support, and implementing this ensures customers can get help through their preferred method.

**Independent Test**: Can be fully tested by sending an email to the support address and verifying that the system processes it and sends an appropriate response, delivering value by automating email support.

**Acceptance Scenarios**:

1. **Given** an incoming email from a customer, **When** the system processes it, **Then** it sends a relevant response via email within the expected timeframe
2. **Given** an incoming email with a complex issue, **When** the AI determines it cannot be resolved automatically, **Then** it marks the ticket for escalation to human support

---

### User Story 3 - Receive AI Response via WhatsApp (Priority: P2)

A customer sends a message via WhatsApp to the support number and expects a timely response. The system receives the WhatsApp message, processes it with the AI agent, and sends back a helpful response through the same channel.

**Why this priority**: WhatsApp is an increasingly popular communication channel, especially for mobile-first users, expanding the reach of the support system.

**Independent Test**: Can be fully tested by sending a WhatsApp message to the support number and verifying that the system processes it and sends an appropriate response.

**Acceptance Scenarios**:

1. **Given** an incoming WhatsApp message from a customer, **When** the system processes it, **Then** it sends a relevant response via WhatsApp within the expected timeframe

---

### User Story 4 - Track Ticket Status (Priority: P2)

A customer who submitted a request wants to check the status of their ticket. They can enter their ticket ID on the website and see the current status and any messages exchanged in the conversation thread.

**Why this priority**: Providing visibility into ticket status improves customer satisfaction and reduces duplicate inquiries.

**Independent Test**: Can be fully tested by entering a valid ticket ID and viewing the associated status and conversation history.

**Acceptance Scenarios**:

1. **Given** a customer with a ticket ID, **When** they enter it on the status page, **Then** they see the current status and conversation history
2. **Given** a customer with an invalid ticket ID, **When** they enter it on the status page, **Then** they receive an appropriate error message

---

### User Story 5 - Cross-Channel Customer Identification (Priority: P3)

A customer contacts support via email first, then follows up via WhatsApp using the same email address or phone number. The system recognizes them as the same customer and maintains conversation continuity.

**Why this priority**: While important for a seamless experience, this can be implemented after the basic channels are working.

**Independent Test**: Can be tested by creating a conversation via one channel and continuing it via another, verifying that the system maintains context.

**Acceptance Scenarios**:

1. **Given** a customer who previously contacted via email, **When** they contact via WhatsApp with the same email or phone, **Then** the system links both conversations to the same customer record

---

### Edge Cases

- What happens when the AI system is temporarily unavailable?
- How does the system handle extremely long or malformed messages?
- What occurs when a customer tries to submit multiple identical requests rapidly?
- How does the system handle messages in unsupported languages?
- What happens when the 24-hour conversation window expires?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST accept support requests via web form with fields for Name, Email, Category, and Message
- **FR-002**: System MUST validate web form inputs according to specified rules (name: 2-50 chars, email: valid format, message: 20-1000 chars)
- **FR-003**: System MUST process incoming emails from Gmail and respond appropriately
- **FR-004**: System MUST process incoming WhatsApp messages via Twilio and respond appropriately
- **FR-005**: System MUST use AI to understand customer intent and generate helpful responses
- **FR-006**: System MUST escalate requests to human support when the AI cannot resolve them automatically
- **FR-007**: System MUST identify customers across channels using email as primary identifier
- **FR-008**: System MUST maintain conversation context for 24 hours before starting a new conversation
- **FR-009**: System MUST assign and display unique ticket IDs for tracking purposes
- **FR-010**: System MUST store all conversations and messages for audit and learning purposes
- **FR-011**: System MUST provide a web interface for customers to check ticket status
- **FR-012**: System MUST log metrics including response time, sentiment score, and escalation rate

### Key Entities *(include if feature involves data)*

- **Customer**: Represents a unique individual seeking support; identified primarily by email, secondarily by phone number
- **Ticket**: Represents a single support request with status, creation time, and resolution status
- **Conversation**: A collection of related messages between customer and support system within a 24-hour window
- **Message**: An individual communication in a conversation, with timestamp, sender, and content
- **Category**: Classification of support request (General, Technical, Billing, Feedback, Bug Report)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Customers receive an initial response to their support request within 2 minutes of submission
- **SC-002**: The AI system successfully resolves at least 75% of support requests without human intervention
- **SC-003**: At least 90% of customers can successfully submit a support request through the web form
- **SC-004**: The system correctly identifies and links 95% of customers who use multiple channels
- **SC-005**: Customer satisfaction rating for support interactions is above 80%
- **SC-006**: The system maintains 99% uptime during business hours

## Outcome

- ✅ Impact: Created comprehensive specification for multi-channel AI support system
- 🧪 Tests: No automated tests for specification creation
- 📁 Files: Created spec.md and requirements checklist
- 🔁 Next prompts: Proceed with planning phase (/sp.plan)
- 🧠 Reflection: Specification covers all key aspects of the multi-channel support system with clear user stories, requirements, and success criteria

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin implementation planning