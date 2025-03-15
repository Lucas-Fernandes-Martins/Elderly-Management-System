import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_username = os.getenv("SMTP_USERNAME", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.from_email = os.getenv("FROM_EMAIL", "noreply@elderlycare.com")
        self.from_name = os.getenv("FROM_NAME", "Elderly Care System")

    def send_email(self, to_email, subject, message):
        """
        Send an email using SMTP
        """
        try:
            # Create message
            msg = MIMEMultipart()
            msg["From"] = f"{self.from_name} <{self.from_email}>"
            msg["To"] = to_email
            msg["Subject"] = subject

            # Add message body
            msg.attach(MIMEText(message, "html"))

            # Connect to SMTP server
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.smtp_username, self.smtp_password)

            # Send email
            server.send_message(msg)
            server.quit()

            logger.info(f"Email sent to {to_email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False

    def send_reminder(self, to_email, elderly_name, subject, message):
        """
        Send a reminder email about an elderly person
        """
        html_message = f"""
        <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background-color: #1976d2; color: white; padding: 10px; text-align: center; }}
                    .content {{ padding: 20px; background-color: #f9f9f9; }}
                    .footer {{ text-align: center; margin-top: 20px; font-size: 12px; color: #777; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h2>Lembrete de Acompanhamento</h2>
                    </div>
                    <div class="content">
                        <p>Olá,</p>
                        <p>Este é um lembrete para o acompanhamento de <strong>{elderly_name}</strong>.</p>
                        <p>{message}</p>
                        <p>Obrigado por seu trabalho no cuidado aos idosos!</p>
                    </div>
                    <div class="footer">
                        <p>Este é um email automático. Por favor, não responda.</p>
                        <p>© {self.from_name}</p>
                    </div>
                </div>
            </body>
        </html>
        """
        return self.send_email(to_email, subject, html_message)


# Create a singleton instance
email_service = EmailService() 