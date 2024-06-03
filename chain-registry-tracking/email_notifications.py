import smtplib, ssl
from email.message import EmailMessage
from dotenv import load_dotenv
import os
from email.mime.text import MIMEText
from loguru import logger

class EmailConfig():
    def __init__(self):
        load_dotenv()
        self.password=os.environ.get("EMAIL_PASSWORD")
        self.username = os.environ.get("EMAIL_USERNAME")
        self.smtp_server_name=os.environ.get("SMTP_SERVER")
        self.port=int(os.environ.get("SMTP_SERVER_PORT"))
        self.sender=os.environ.get("EMAIL_SENDER")


def send_email(email_config: EmailConfig, recipients : list, msg):

    with smtplib.SMTP(email_config.smtp_server_name, email_config.port) as server:
        server.starttls()
        server.login(email_config.username, email_config.password)
        server.sendmail(email_config.sender,recipients,msg)
        logger.info(f"message sent to {recipients}")
        server.quit()


def format_email(subject, body, sender, recipients) -> str:
    msg=MIMEText(body)
    msg["Subject"]=subject
    msg["From"] = sender
    msg["To"] = ",".join(recipients)
    return msg.as_string()


def main(subject: str, msg_body: str, recipients: list):
    email_config = EmailConfig()
    sender = email_config.sender
    msg=format_email(subject, msg_body, sender, recipients)
    send_email(email_config, recipients, msg)
