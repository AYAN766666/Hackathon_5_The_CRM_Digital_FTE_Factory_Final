"""
Email Service - Send support confirmation emails via Gmail SMTP
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from config import settings


class EmailService:
    """Handle email sending for support tickets"""
    
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = settings.gmail_email
        self.sender_password = settings.gmail_app_password
    
    async def send_support_email(
        self,
        customer_email: str,
        ticket_id: str,
        ai_response: str,
        customer_name: Optional[str] = None
    ) -> bool:
        """
        Send support ticket confirmation email
        
        Args:
            customer_email: Recipient email address
            ticket_id: Support ticket ID
            ai_response: AI generated response message
            customer_name: Optional customer name
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            # Create message
            msg = MIMEMultipart("alternative")
            msg["Subject"] = f"Support Ticket Created - {ticket_id}"
            msg["From"] = self.sender_email
            msg["To"] = customer_email
            
            # Create email content
            name_str = customer_name if customer_name else "Valued Customer"
            
            html_content = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #2563eb;">Support Ticket Confirmation</h2>
                    
                    <p>Dear {name_str},</p>
                    
                    <p>Thank you for contacting our support team. Your ticket has been created successfully.</p>
                    
                    <div style="background-color: #f3f4f6; padding: 15px; border-radius: 8px; margin: 20px 0;">
                        <p><strong>Ticket ID:</strong> {ticket_id}</p>
                    </div>
                    
                    <h3>Our Response:</h3>
                    <div style="background-color: #e0f2fe; padding: 15px; border-radius: 8px; margin: 15px 0;">
                        <p>{ai_response}</p>
                    </div>
                    
                    <p>Our team is reviewing your request and will get back to you shortly if further assistance is needed.</p>
                    
                    <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 20px 0;">
                    
                    <p style="color: #6b7280; font-size: 14px;">
                        Best regards,<br>
                        <strong>Customer Success Team</strong>
                    </p>
                </div>
            </body>
            </html>
            """
            
            text_content = f"""
            Support Ticket Confirmation
            
            Dear {name_str},
            
            Thank you for contacting our support team. Your ticket has been created successfully.
            
            Ticket ID: {ticket_id}
            
            Our Response:
            {ai_response}
            
            Our team is reviewing your request and will get back to you shortly if further assistance is needed.
            
            Best regards,
            Customer Success Team
            """
            
            # Attach both plain text and HTML versions
            msg.attach(MIMEText(text_content, "plain"))
            msg.attach(MIMEText(html_content, "html"))
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, customer_email, msg.as_string())
            server.quit()

            print(f"[OK] Email sent to {customer_email} for ticket {ticket_id}")
            return True

        except Exception as e:
            print(f"[ERROR] Error sending email: {str(e)}")
            return False


# Singleton instance
email_service = EmailService()
