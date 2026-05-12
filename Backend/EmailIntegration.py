# Backend/EmailIntegration.py
import imaplib
import ssl
import smtplib
import os
import email
from email.mime.text import MIMEText
from dotenv import dotenv_values
from datetime import datetime

# Load environment variables
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_vars = dotenv_values(os.path.join(current_dir, ".env"))

IMAP_SERVER = env_vars.get("IMAP_SERVER", "imap.gmail.com")
IMAP_PORT = int(env_vars.get("IMAP_PORT", 993))
EMAIL_ADDRESS = env_vars.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = env_vars.get("EMAIL_PASSWORD")

SMTP_SERVER = env_vars.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(env_vars.get("SMTP_PORT", 587))
SMTP_USE_TLS = env_vars.get("SMTP_USE_TLS", "True").lower() == "true"

class EmailClient:
    def __init__(self):
        self.email = EMAIL_ADDRESS
        self.password = EMAIL_PASSWORD

    def get_imap_connection(self):
        try:
            if not self.email or not self.password:
                return None, "Email credentials missing."
            context = ssl.create_default_context()
            mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT, ssl_context=context)
            mail.login(self.email, self.password)
            return mail, None
        except Exception as e:
            return None, str(e)

    def check_emails(self, limit=5):
        mail, error = self.get_imap_connection()
        if error: return f"Error: {error}"
        try:
            mail.select('inbox')
            _, data = mail.search(None, 'ALL')
            ids = data[0].split()
            results = []
            for num in reversed(ids[-limit:]):
                _, msg_data = mail.fetch(num, '(RFC822)')
                msg = email.message_from_bytes(msg_data[0][1])
                results.append({
                    "sender": msg.get("from"),
                    "subject": msg.get("subject"),
                    "date": msg.get("date")
                })
            mail.logout()
            return results
        except Exception as e:
            return f"Error fetching emails: {e}"

    def send_email(self, recipient, subject, body):
        if not self.email or not self.password:
            return "Email credentials missing."
        try:
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = self.email
            msg['To'] = recipient
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            if SMTP_USE_TLS: server.starttls()
            server.login(self.email, self.password)
            server.sendmail(self.email, recipient, msg.as_string())
            server.quit()
            return f"Sent to {recipient}"
        except Exception as e:
            return f"Error sending: {e}"

    def summarize_emails(self, limit=10):
        return "Summarization not yet implemented."
