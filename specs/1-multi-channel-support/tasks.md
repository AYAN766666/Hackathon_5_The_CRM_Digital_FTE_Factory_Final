# Tasks: Multi-Channel AI Support System

**Feature**: 1-multi-channel-support
**Created**: 2026-03-12
**Status**: Draft

## Phase 1: Setup Tasks

- [ ] T001 Create project structure with backend and frontend directories
- [ ] T002 [P] Set up Python virtual environment and install dependencies (fastapi, uvicorn, asyncpg, aiokafka, python-multipart)
- [ ] T003 [P] Set up Node.js project and install dependencies (next, react, react-dom)
- [ ] T004 [P] Configure environment variables for API keys and connection strings
- [ ] T005 Set up Docker configuration for local Kafka development
- [ ] T006 [P] Create initial project documentation files (README.md, .gitignore, requirements.txt, package.json)

## Phase 2: Foundational Tasks

- [ ] T007 [P] Create database models for Customer entity in backend/models/customer.py
- [ ] T008 [P] Create database models for CustomerIdentifier entity in backend/models/customer_identifier.py
- [ ] T009 [P] Create database models for Conversation entity in backend/models/conversation.py
- [ ] T010 [P] Create database models for Message entity in backend/models/message.py
- [ ] T011 Create database initialization script in backend/database.py
- [ ] T012 [P] Set up Kafka producer in backend/services/kafka_producer.py
- [ ] T013 [P] Set up Kafka consumer in backend/services/kafka_consumer.py
- [ ] T014 Set up AI integration service using Gemini API in backend/services/ai_service.py
- [ ] T015 Create customer service in backend/services/customer_service.py
- [ ] T016 Create conversation service in backend/services/conversation_service.py
- [ ] T017 Create message service in backend/services/message_service.py

## Phase 3: User Story 1 - Submit Support Request via Web Form (Priority: P1)

**Goal**: Enable customers to submit support requests via web form with validation and ticket creation.

**Independent Test**: Can be fully tested by filling out the web form and verifying that a ticket is created with proper validation, showing the ticket ID to the user, and delivering immediate value by capturing customer requests.

**Implementation Tasks**:

- [ ] T018 [P] [US1] Create SupportForm component in frontend/components/SupportForm.tsx
- [ ] T019 [P] [US1] Create support page in frontend/app/support/page.tsx
- [ ] T020 [P] [US1] Implement form validation logic in frontend/components/SupportForm.tsx
- [ ] T021 [P] [US1] Add styling with gradient buttons and 3D effects to SupportForm.tsx
- [ ] T022 [US1] Create POST /support/submit endpoint in backend/routes/webform.py
- [ ] T023 [US1] Implement validation logic in /support/submit endpoint according to FR-002
- [ ] T024 [US1] Connect web form to Kafka producer to push messages to fte.tickets.incoming
- [ ] T025 [US1] Create ticket ID generation and return it to frontend
- [ ] T026 [US1] Implement customer creation logic if new customer in customer_service.py
- [ ] T027 [US1] Update frontend to show success message with ticket ID in green (#28A745)

## Phase 4: User Story 2 - Receive AI Response via Email (Priority: P1)

**Goal**: Process incoming emails from Gmail, process with AI agent, and send appropriate responses.

**Independent Test**: Can be fully tested by sending an email to the support address and verifying that the system processes it and sends an appropriate response, delivering value by automating email support.

**Implementation Tasks**:

- [ ] T028 [P] [US2] Create email webhook handler in backend/routes/email.py
- [ ] T029 [P] [US2] Implement email parsing logic in backend/services/email_parser.py
- [ ] T030 [US2] Create POST /webhooks/gmail endpoint to receive notifications
- [ ] T031 [US2] Connect email webhook to Kafka producer to push messages to fte.tickets.incoming
- [ ] T032 [US2] Implement email response logic in backend/services/email_responder.py
- [ ] T033 [US2] Integrate with AI service for message understanding and response generation
- [ ] T034 [US2] Implement escalation logic when AI cannot resolve automatically (FR-006)
- [ ] T035 [US2] Add metrics logging for email responses to fte.metrics

## Phase 5: User Story 3 - Receive AI Response via WhatsApp (Priority: P2)

**Goal**: Process incoming WhatsApp messages via Twilio, process with AI agent, and send appropriate responses.

**Independent Test**: Can be fully tested by sending a WhatsApp message to the support number and verifying that the system processes it and sends an appropriate response.

**Implementation Tasks**:

- [ ] T036 [P] [US3] Create WhatsApp webhook handler in backend/routes/whatsapp.py
- [ ] T037 [P] [US3] Implement Twilio signature validation in WhatsApp handler
- [ ] T038 [US3] Create POST /webhooks/whatsapp endpoint to receive notifications
- [ ] T039 [US3] Connect WhatsApp webhook to Kafka producer to push messages to fte.tickets.incoming
- [ ] T040 [US3] Implement WhatsApp response logic in backend/services/whatsapp_responder.py
- [ ] T041 [US3] Integrate with AI service for message understanding and response generation
- [ ] T042 [US3] Implement escalation logic for WhatsApp messages
- [ ] T043 [US3] Add metrics logging for WhatsApp responses to fte.metrics

## Phase 6: User Story 4 - Track Ticket Status (Priority: P2)

**Goal**: Allow customers to check the status of their ticket using ticket ID.

**Independent Test**: Can be fully tested by entering a valid ticket ID and viewing the associated status and conversation history.

**Implementation Tasks**:

- [ ] T044 [P] [US4] Create ticket status modal component in frontend/components/TicketStatusModal.tsx
- [ ] T045 [P] [US4] Add status button with green color (#28A745) to SupportForm.tsx
- [ ] T046 [US4] Create GET /support/ticket/{ticket_id} endpoint in backend/routes/webform.py
- [ ] T047 [US4] Implement ticket retrieval logic with conversation history
- [ ] T048 [US4] Add proper error handling for invalid ticket IDs
- [ ] T049 [US4] Update frontend to display color-coded messages in the status modal

## Phase 7: User Story 5 - Cross-Channel Customer Identification (Priority: P3)

**Goal**: Identify customers across channels using email as primary identifier and maintain conversation continuity.

**Independent Test**: Can be tested by creating a conversation via one channel and continuing it via another, verifying that the system maintains context.

**Implementation Tasks**:

- [ ] T050 [US5] Enhance customer service to implement cross-channel identification logic
- [ ] T051 [US5] Update message processor to resolve customer by email/phone across channels
- [ ] T052 [US5] Implement logic to link conversations from same customer across channels
- [ ] T053 [US5] Update conversation service to handle 24-hour window logic (FR-008)
- [ ] T054 [US5] Add customer identification to email processing workflow
- [ ] T055 [US5] Add customer identification to WhatsApp processing workflow

## Phase 8: Message Processing Worker

**Goal**: Create a worker that consumes messages from Kafka, processes them with AI, and manages conversations.

**Implementation Tasks**:

- [ ] T056 [P] Create message processor worker in backend/workers/message_processor.py
- [ ] T057 [P] Implement Kafka consumer logic in message processor
- [ ] T058 Connect message processor to AI service for intent classification
- [ ] T059 Implement conversation context retrieval in message processor
- [ ] T060 Add response generation logic to message processor
- [ ] T061 Implement escalation detection in message processor
- [ ] T062 Add error handling with graceful fallback to message processor
- [ ] T063 Implement DLQ handling for failed messages

## Phase 9: Metrics and Monitoring

**Goal**: Implement metrics tracking and monitoring for system performance.

**Implementation Tasks**:

- [ ] T064 [P] Create metrics service in backend/services/metrics_service.py
- [ ] T065 Add latency tracking to message processing
- [ ] T066 Implement sentiment scoring in AI service
- [ ] T067 Add escalation tracking to metrics service
- [ ] T068 Publish metrics to fte.metrics Kafka topic
- [ ] T069 Update message models to include metrics fields

## Phase 10: Polish & Cross-Cutting Concerns

- [ ] T070 [P] Add comprehensive error handling throughout the system
- [ ] T071 Implement graceful degradation when AI service unavailable
- [ ] T072 Add logging throughout the application
- [ ] T073 Set up health check endpoints
- [ ] T074 Add input sanitization to prevent injection attacks
- [ ] T075 Create deployment configurations for Kubernetes
- [ ] T076 Write comprehensive API documentation
- [ ] T077 Update README with setup and usage instructions

## Dependencies

**User Story Order**:
1. User Story 1 (Web Form) - Foundation for all other stories
2. User Story 2 (Email) - Can work independently after foundation
3. User Story 3 (WhatsApp) - Can work independently after foundation
4. User Story 4 (Status) - Depends on Stories 1-3 (needs tickets/messages to exist)
5. User Story 5 (Cross-channel) - Depends on Stories 2-3 (needs multiple channels)

## Parallel Execution Examples

**Per User Story**:
- **US1**: UI development (SupportForm.tsx) can run in parallel with backend endpoint development (/support/submit)
- **US2**: Email parsing service can be developed in parallel with webhook endpoint
- **US3**: WhatsApp responder service can be developed in parallel with webhook endpoint
- **US4**: Frontend modal component can be developed in parallel with backend endpoint
- **US5**: Customer identification logic can be developed in parallel with conversation management

## Implementation Strategy

**MVP First**: Implement User Story 1 (Web Form) with minimal viable functionality to create tickets and return IDs.

**Incremental Delivery**:
1. Complete Phase 1-3 (Setup + Web Form) as first deliverable
2. Add Email handling (US2) as second deliverable
3. Add WhatsApp handling (US3) as third deliverable
4. Add status tracking (US4) as fourth deliverable
5. Add cross-channel features (US5) as fifth deliverable