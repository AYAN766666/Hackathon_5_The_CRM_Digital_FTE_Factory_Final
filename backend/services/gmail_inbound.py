"""
Gmail Inbound Service - Receive and process incoming emails
"""
import os
import sys
import email
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import asyncio
import re

# Add parent path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from config import settings
from services.ai_service import ai_service
from services.customer_service import customer_service
from services.conversation_service import conversation_service
from services.message_service import message_service
from services.kafka_producer import kafka_producer
from models import ChannelType, SenderType


class GmailInboundService:
    """
    Gmail Inbound Service - Process incoming support emails
    
    Features:
    - Connect to Gmail via IMAP
    - Fetch unread emails from support inbox
    - Parse email content
    - Generate AI response
    - Send reply
    - Create/update tickets
    """

    def __init__(self):
        self.imap_server = "imap.gmail.com"
        self.imap_port = 993
        self.email_address = settings.gmail_email
        self.app_password = settings.gmail_app_password
        self.support_folder = "INBOX"  # Can be changed to specific folder

    def connect(self) -> imaplib.IMAP4_SSL:
        """Connect to Gmail IMAP server"""
        try:
            mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            mail.login(self.email_address, self.app_password)
            print(f"✅ Connected to Gmail: {self.email_address}")
            return mail
        except Exception as e:
            print(f"❌ Gmail connection error: {str(e)}")
            raise

    def fetch_unread_emails(self, mail: imaplib.IMAP4_SSL, limit: int = 10) -> List[Dict[str, Any]]:
        """Fetch unread emails from inbox"""
        emails = []
        
        try:
            # Select inbox
            mail.select(self.support_folder)
            
            # Search for unread emails
            status, messages = mail.search(None, "UNSEEN")
            
            if status != "OK":
                print("No unread emails found")
                return emails
            
            # Get message IDs
            email_ids = messages[0].split()
            
            # Limit number of emails to process
            email_ids = email_ids[-limit:]  # Last N emails
            
            for email_id in email_ids:
                try:
                    # Fetch email
                    status, msg_data = mail.fetch(email_id, "(RFC822)")
                    
                    if status != "OK":
                        continue
                    
                    # Parse email
                    raw_email = msg_data[0][1]
                    email_message = email.message_from_bytes(raw_email)
                    
                    # Extract email data
                    email_data = self._parse_email(email_message, email_id)
                    
                    if email_data:
                        emails.append(email_data)
                        
                except Exception as e:
                    print(f"Error parsing email {email_id}: {str(e)}")
            
            return emails
            
        except Exception as e:
            print(f"Error fetching emails: {str(e)}")
            return emails

    def _parse_email(self, email_message: email.message.Message, email_id: bytes) -> Optional[Dict[str, Any]]:
        """Parse email message"""
        try:
            # Extract headers
            subject = email_message.get("Subject", "No Subject")
            from_address = email_message.get("From", "")
            to_address = email_message.get("To", "")
            date_str = email_message.get("Date", "")
            
            # Parse from address to get email and name
            from_name = ""
            from_email = ""
            
            if "<" in from_address and ">" in from_address:
                match = re.match(r"(.+?)\s*<(.+?)>", from_address)
                if match:
                    from_name = match.group(1).strip()
                    from_email = match.group(2).strip()
            else:
                from_email = from_address.strip()
            
            # Get email body
            body = ""
            if email_message.is_multipart():
                # Get plain text part
                for part in email_message.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition", ""))
                    
                    # Skip attachments
                    if "attachment" in content_disposition:
                        continue
                    
                    if content_type == "text/plain":
                        try:
                            body = part.get_payload(decode=True).decode()
                            break
                        except:
                            pass
            else:
                # Plain text email
                try:
                    body = email_message.get_payload(decode=True).decode()
                except:
                    pass
            
            # Parse date
            try:
                date_parsed = email.utils.parsedate_to_datetime(date_str)
            except:
                date_parsed = datetime.now()
            
            return {
                "email_id": email_id.decode(),
                "subject": subject,
                "from_email": from_email,
                "from_name": from_name,
                "to_email": to_address,
                "date": date_parsed,
                "body": body,
                "raw_message": email_message
            }
            
        except Exception as e:
            print(f"Error parsing email: {str(e)}")
            return None

    async def process_email(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process incoming email and generate response
        
        Args:
            email_data: Parsed email data
            
        Returns:
            Processing result
        """
        try:
            from_email = email_data.get("from_email")
            from_name = email_data.get("from_name")
            subject = email_data.get("subject")
            body = email_data.get("body")
            
            if not from_email or not body:
                return {"success": False, "error": "Missing email or body"}
            
            # Combine subject and body for context
            full_message = f"Subject: {subject}\n\n{body}"
            
            # Get or create customer
            customer = await customer_service.get_or_create_customer(
                email=from_email,
                name=from_name if from_name else None
            )
            
            # Get or create conversation
            conversation = await conversation_service.get_or_create_conversation(
                customer_id=customer.customer_id,
                channel=ChannelType.email
            )
            
            # Save customer message
            await message_service.create_message(
                conversation_id=conversation.conversation_id,
                content=full_message,
                sender_type=SenderType.customer,
                sender_identifier=from_email
            )
            
            # Generate AI response
            ai_response = await ai_service.generate_response(
                customer_message=body,
                category="General",
                channel="email"
            )
            
            # Save AI response
            await message_service.create_message(
                conversation_id=conversation.conversation_id,
                content=ai_response["response"],
                sender_type=SenderType.agent,
                sender_identifier="AI Agent",
                sentiment_score=ai_response.get("sentiment_score"),
                escalation_required=ai_response.get("escalation_required", False)
            )
            
            # Send email response
            from services.email_service import email_service
            
            ticket_id = str(conversation.conversation_id)[:8].upper()
            
            email_sent = await email_service.send_support_email(
                customer_email=from_email,
                ticket_id=ticket_id,
                ai_response=ai_response["response"],
                customer_name=from_name
            )
            
            # Publish Kafka event
            await kafka_producer.publish_ticket_created(
                ticket_id=ticket_id,
                customer_email=from_email,
                channel="email",
                category="General"
            )
            
            # Mark email as read
            self._mark_as_read(email_data.get("email_id"))
            
            # Handle escalation
            if ai_response.get("escalation_required"):
                await conversation_service.escalate_conversation(
                    conversation_id=conversation.conversation_id
                )
                
                await kafka_producer.publish_ticket_escalated(
                    ticket_id=ticket_id,
                    reason="AI detected complex issue"
                )
            
            return {
                "success": True,
                "ticket_id": ticket_id,
                "response_sent": email_sent,
                "escalation_required": ai_response.get("escalation_required", False)
            }
            
        except Exception as e:
            print(f"Error processing email: {str(e)}")
            return {"success": False, "error": str(e)}

    def _mark_as_read(self, email_id: str):
        """Mark email as read"""
        try:
            mail = self.connect()
            mail.store(email_id.encode(), "+FLAGS", "\\Seen")
            mail.close()
            mail.logout()
        except Exception as e:
            print(f"Error marking email as read: {str(e)}")

    async def process_inbox(self, limit: int = 10) -> Dict[str, Any]:
        """
        Process all unread emails in inbox
        
        Args:
            limit: Maximum number of emails to process
            
        Returns:
            Processing summary
        """
        results = {
            "processed": 0,
            "success": 0,
            "failed": 0,
            "errors": []
        }
        
        try:
            mail = self.connect()
            emails = self.fetch_unread_emails(mail, limit)
            mail.close()
            mail.logout()
            
            print(f"📧 Found {len(emails)} unread emails")
            
            for email_data in emails:
                results["processed"] += 1
                
                process_result = await self.process_email(email_data)
                
                if process_result.get("success"):
                    results["success"] += 1
                    print(f"✅ Processed email from {email_data.get('from_email')}")
                else:
                    results["failed"] += 1
                    results["errors"].append({
                        "email": email_data.get("from_email"),
                        "error": process_result.get("error")
                    })
                    print(f"❌ Failed to process email: {process_result.get('error')}")
            
            return results
            
        except Exception as e:
            print(f"Error processing inbox: {str(e)}")
            results["errors"].append(str(e))
            return results


# Singleton instance
gmail_inbound = GmailInboundService()


async def process_incoming_emails(limit: int = 10):
    """Process incoming emails"""
    return await gmail_inbound.process_inbox(limit)
