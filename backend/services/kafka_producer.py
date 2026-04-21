"""
Kafka Producer Service - Publish ticket events to Kafka
"""
import os
import sys
import json
from typing import Dict, Any, Optional
from datetime import datetime
from aiokafka import AIOKafkaProducer
import asyncio

# Add parent path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from config import settings


class KafkaProducerService:
    """
    Kafka Producer for publishing ticket events
    
    Topics:
    - fte.tickets.incoming: New ticket created
    - fte.tickets.updated: Ticket status updated
    - fte.tickets.escalated: Ticket escalated to human
    - fte.metrics: System metrics
    """

    def __init__(self):
        self.producer: Optional[AIOKafkaProducer] = None
        self.bootstrap_servers = settings.kafka_bootstrap_servers
        self.topic_tickets = settings.kafka_topic_tickets
        self.topic_metrics = settings.kafka_topic_metrics
        self.is_connected = False

    async def start(self):
        """Start Kafka producer"""
        try:
            print(f"[INFO] Connecting to Kafka at {self.bootstrap_servers}...")

            self.producer = AIOKafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                key_serializer=lambda k: k.encode('utf-8') if k else None,
                acks='all',  # Wait for all replicas to acknowledge
                retries=3,
                retry_backoff_ms=100,
                connections_max_idle_ms=5000
            )

            await self.producer.start()
            self.is_connected = True

            print(f"[OK] Kafka producer connected to {self.bootstrap_servers}")
            return True

        except Exception as e:
            error_msg = str(e)
            print(f"[WARN] Kafka connection failed: {error_msg}")
            
            # Provide helpful error messages
            if "getaddrinfo" in error_msg or "Name or service not known" in error_msg:
                print("\n[WARN] NETWORK ERROR: Cannot resolve Kafka hostname")
                print("   Kafka is optional - system will work without it")
                print("   To enable Kafka:")
                print("   1. Make sure Kafka is installed and running")
                print("   2. Check KAFKA_BOOTSTRAP_SERVERS in .env file")
            elif "connection refused" in error_msg.lower():
                print("\n[WARN] CONNECTION ERROR: Kafka refused connection")
                print("   Kafka is optional - system will work without it")
                print("   To enable Kafka:")
                print("   1. Make sure Kafka is running on the configured host/port")
                print("   2. Check KAFKA_BOOTSTRAP_SERVERS in .env file")
            elif "NoBrokersAvailable" in error_msg:
                print("\n[WARN] KAFKA ERROR: No Kafka brokers available")
                print("   Kafka is optional - system will work without it")
            else:
                print("\n[INFO] Running without Kafka - events will not be published")
            
            self.is_connected = False
            return False

    async def stop(self):
        """Stop Kafka producer"""
        if self.producer:
            await self.producer.stop()
            self.is_connected = False
            print("🛑 Kafka producer stopped")

    async def publish_ticket_event(
        self,
        event_type: str,
        ticket_id: str,
        data: Dict[str, Any]
    ):
        """
        Publish ticket event to Kafka
        
        Args:
            event_type: Type of event (created, updated, escalated)
            ticket_id: Ticket ID
            data: Event data
        """
        if not self.is_connected:
            print(f"⚠️ Kafka not connected, skipping event: {event_type}")
            return False

        try:
            message = {
                "event_type": event_type,
                "ticket_id": ticket_id,
                "timestamp": datetime.utcnow().isoformat(),
                "data": data
            }

            await self.producer.send_and_wait(
                topic=self.topic_tickets,
                value=message,
                key=ticket_id
            )

            print(f"📤 Published event {event_type} for ticket {ticket_id}")
            return True

        except Exception as e:
            print(f"❌ Error publishing event: {str(e)}")
            return False

    async def publish_ticket_created(
        self,
        ticket_id: str,
        customer_email: str,
        channel: str,
        category: str,
        **kwargs
    ):
        """Publish ticket created event"""
        return await self.publish_ticket_event(
            event_type="created",
            ticket_id=ticket_id,
            data={
                "customer_email": customer_email,
                "channel": channel,
                "category": category,
                **kwargs
            }
        )

    async def publish_ticket_updated(
        self,
        ticket_id: str,
        status: str,
        **kwargs
    ):
        """Publish ticket updated event"""
        return await self.publish_ticket_event(
            event_type="updated",
            ticket_id=ticket_id,
            data={
                "status": status,
                **kwargs
            }
        )

    async def publish_ticket_escalated(
        self,
        ticket_id: str,
        reason: str,
        escalated_to: str = "human_agent",
        **kwargs
    ):
        """Publish ticket escalated event"""
        return await self.publish_ticket_event(
            event_type="escalated",
            ticket_id=ticket_id,
            data={
                "reason": reason,
                "escalated_to": escalated_to,
                **kwargs
            }
        )

    async def publish_metric(
        self,
        metric_name: str,
        value: float,
        labels: Optional[Dict[str, str]] = None
    ):
        """
        Publish system metric to Kafka
        
        Args:
            metric_name: Metric name (e.g., response_time_ms)
            value: Metric value
            labels: Additional labels
        """
        if not self.is_connected:
            return False

        try:
            message = {
                "metric_name": metric_name,
                "value": value,
                "timestamp": datetime.utcnow().isoformat(),
                "labels": labels or {}
            }

            await self.producer.send_and_wait(
                topic=self.topic_metrics,
                value=message,
                key=metric_name
            )

            return True

        except Exception as e:
            print(f"❌ Error publishing metric: {str(e)}")
            return False


# Singleton instance
kafka_producer = KafkaProducerService()


async def get_kafka_producer() -> KafkaProducerService:
    """Get Kafka producer instance"""
    return kafka_producer


async def initialize_kafka():
    """Initialize Kafka producer"""
    await kafka_producer.start()
    return kafka_producer


async def shutdown_kafka():
    """Shutdown Kafka producer"""
    await kafka_producer.stop()
