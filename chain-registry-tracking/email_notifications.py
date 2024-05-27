import smtplib, ssl
from email.message import EmailMessage
from dotenv import load_dotenv
import os

def send_email(to_email, subject, msg):

    ##CONFIG CONSTANTS
    load_dotenv()
    email_password = os.environ.get("EMAIL_PASSWORD")
    email_username=os.environ.get("EMAIL_USERNAME")
    smtp_server_name=os.environ.get("SMTP_SERVER")#"smtp.gmail.com"
    port = 465 #465 for SSL


    message= EmailMessage()
    message['Subject'] = subject
    message['From']= email_username
    message['To']=to_email
    message.set_content(msg)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server_name, port, context=context) as server:
        server.login(email_username,email_password)
        server.send_message(message)
        server.quit()

