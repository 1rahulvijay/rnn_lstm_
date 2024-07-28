import os
import json
import logging
from typing import List, Dict, Optional
from pydantic import BaseSettings
from jinja2 import Environment, FileSystemLoader
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

# Configuration settings using pydantic
class Settings(BaseSettings):
    smtp_server: str
    smtp_port: int
    smtp_user: str
    smtp_password: str
    default_subject: str
    attachments_dir: str
    templates_dir: str
    log_file: str

    class Config:
        env_file = '.env'

settings = Settings()

# Configure logging
logging.basicConfig(filename=settings.log_file, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class EmailSender:
    def __init__(self):
        # Set up Jinja2 environment
        self.env = Environment(loader=FileSystemLoader(settings.templates_dir))

    def load_template(self, template_name: str, context: Dict[str, str]) -> str:
        try:
            template = self.env.get_template(template_name)
            return template.render(context)
        except Exception as e:
            logging.error(f"Error loading template {template_name}: {e}")
            raise

    def send_email(self, to_email: str, subject: str, body: str, attachments: List[str] = []):
        msg = MIMEMultipart()
        msg['From'] = settings.smtp_user
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'html'))

        for file_path in attachments:
            if os.path.isfile(file_path):
                try:
                    part = MIMEBase('application', 'octet-stream')
                    with open(file_path, 'rb') as file:
                        part.set_payload(file.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename={os.path.basename(file_path)}'
                    )
                    msg.attach(part)
                except Exception as e:
                    logging.error(f"Error attaching file {file_path}: {e}")
                    raise

        try:
            with smtplib.SMTP(settings.smtp_server, settings.smtp_port) as server:
                server.starttls()
                server.login(settings.smtp_user, settings.smtp_password)
                server.sendmail(settings.smtp_user, to_email, msg.as_string())
                logging.info(f'Email successfully sent to {to_email}')
        except Exception as e:
            logging.error(f'Failed to send email to {to_email}: {e}')
            raise

    def send_bulk_emails(self, recipients: List[Dict[str, Optional[str]]]):
        for recipient in recipients:
            to_email = recipient['email']
            template_name = recipient['template']
            attachments = [os.path.join(settings.attachments_dir, file) for file in recipient.get('attachments', [])]

            context = recipient.get('context', {})
            try:
                body = self.load_template(template_name, context)
                self.send_email(to_email, settings.default_subject, body, attachments)
            except Exception as e:
                logging.error(f"Error processing email for {to_email}: {e}")

if __name__ == '__main__':
    recipients = [
        {
            'email': 'recipient1@example.com',
            'template': 'template1.html',
            'attachments': ['file1.pdf'],
            'context': {'name': 'Alice', 'special_offer': '20% off'}
        },
        {
            'email': 'recipient2@example.com',
            'template': 'template2.html',
            'attachments': ['file2.pdf'],
            'context': {'name': 'Bob', 'special_offer': '30% off'}
        }
    ]

    email_sender = EmailSender()
    email_sender.send_bulk_emails(recipients)
