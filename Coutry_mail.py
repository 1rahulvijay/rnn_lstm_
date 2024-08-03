import os
import json
import logging
from typing import List, Dict, Optional, Union
from pydantic import BaseSettings
from jinja2 import Environment, FileSystemLoader
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import pandas as pd

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

    def send_email(self, to_email: str, subject: str, body: str, attachments: List[Union[str, Dict[str, pd.DataFrame]]] = []):
        msg = MIMEMultipart()
        msg['From'] = settings.smtp_user
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'html'))

        for attachment in attachments:
            if isinstance(attachment, str):
                file_path = attachment
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
            elif isinstance(attachment, dict):
                for filename, df in attachment.items():
                    try:
                        file_path = os.path.join(settings.attachments_dir, filename)
                        df.to_excel(file_path, index=False)
                        part = MIMEBase('application', 'octet-stream')
                        with open(file_path, 'rb') as file:
                            part.set_payload(file.read())
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename={filename}'
                        )
                        msg.attach(part)
                    except Exception as e:
                        logging.error(f"Error attaching DataFrame {filename}: {e}")
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

    def send_bulk_emails(self, recipients: List[Dict[str, Optional[Union[str, pd.DataFrame]]]]):
        for recipient in recipients:
            to_email = recipient['email']
            template_name = recipient['template']
            attachments = []
            for attachment in recipient.get('attachments', []):
                if isinstance(attachment, str):
                    attachments.append(os.path.join(settings.attachments_dir, attachment))
                elif isinstance(attachment, dict):
                    attachments.append(attachment)

            context = recipient.get('context', {})
            try:
                body = self.load_template(template_name, context)
                self.send_email(to_email, settings.default_subject, body, attachments)
            except Exception as e:
                logging.error(f"Error processing email for {to_email}: {e}")

if __name__ == '__main__':
    df = pd.DataFrame({
        'Name': ['Alice', 'Bob'],
        'Special Offer': ['20% off', '30% off']
    })
    
    recipients = [
        {
            'email': 'recipient1@example.com',
            'template': 'template1.html',
            'attachments': ['file1.pdf', {'offer.xlsx': df}],
            'context': {'name': 'Alice', 'special_offer': '20% off'}
        },
        {
            'email': 'recipient2@example.com',
            'template': 'template2.html',
            'attachments': ['file2.pdf', {'offer.xlsx': df}],
            'context': {'name': 'Bob', 'special_offer': '30% off'}
        }
    ]

    email_sender = EmailSender()
    email_sender.send_bulk_emails(recipients)
