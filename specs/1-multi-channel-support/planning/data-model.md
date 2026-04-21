# Data Model: Multi-Channel AI Support System

## Entity: Customer
- customer_id (UUID, primary key)
- email (VARCHAR, unique, indexed)
- phone (VARCHAR, nullable, indexed)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)

## Entity: CustomerIdentifier
- identifier_id (UUID, primary key)
- customer_id (UUID, foreign key)
- identifier_type (ENUM: email, phone, external_id)
- identifier_value (VARCHAR, indexed)
- created_at (TIMESTAMP)

## Entity: Conversation
- conversation_id (UUID, primary key)
- customer_id (UUID, foreign key)
- channel (ENUM: email, whatsapp, webform)
- status (ENUM: active, closed, escalated)
- sentiment_score (FLOAT, nullable)
- started_at (TIMESTAMP)
- last_message_at (TIMESTAMP)
- expires_at (TIMESTAMP)  // 24 hours from last message

## Entity: Message
- message_id (UUID, primary key)
- conversation_id (UUID, foreign key)
- sender_type (ENUM: customer, agent, system)
- sender_identifier (VARCHAR)
- content (TEXT)
- sentiment_score (FLOAT, nullable)
- escalation_required (BOOLEAN)
- created_at (TIMESTAMP)
- processed_latency_ms (INTEGER)

## Relationships
- Customer (1) -> (Many) CustomerIdentifier
- Customer (1) -> (Many) Conversation
- Conversation (1) -> (Many) Message