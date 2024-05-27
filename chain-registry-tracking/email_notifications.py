import smtplib, ssl
from email.message import EmailMessage
from dotenv import load_dotenv
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailConfig():
    def __init__(self):
        load_dotenv()
        self.password=os.environ.get("EMAIL_PASSWORD")
        self.username = os.environ.get("EMAIL_USERNAME")
        self.smtp_server_name=os.environ.get("SMTP_SERVER")
        self.port=587
        self.sender=os.environ.get("EMAIL_SENDER")


def send_email(email_config: EmailConfig, receiver, msg):

    with smtplib.SMTP(email_config.smtp_server_name, email_config.port) as server:
        server.starttls()
        server.login(email_config.username, email_config.password)
        server.sendmail(email_config.sender,receiver,msg)
        print("message sent")
        #server.send_message(message)
        server.quit()

receiver="cmancrypto@outlook.com"
sender="MS_uVEmsW@trial-o65qngkk7qwgwr12.mlsender.net"
message=f"""\
Subject: Chain_Registry_Tracking
To: {receiver}
From: {sender}

Test
"""
email_config=EmailConfig()
print(type(email_config.sender))
send_email(email_config=email_config,receiver=receiver,msg=message)
#todo change to MIME email and then create function to shape message class