import logging
import smtplib
from email.mime.text import MIMEText

from src.celery_app import app
from src.core.config import settings

logger = logging.getLogger(__name__)

@app.task
def send_email(to_email: str, subject: str, body: str):
    logger.info(f"Sending email to {to_email} with subject '{subject}'")
    msg = MIMEText(body, 'plain', 'utf-8')
    msg["Subject"] = subject
    msg["From"] = settings.SMTP_USER
    msg["To"] = to_email

    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(settings.SMTP_USER, to_email, msg.as_string())
            logger.info(f"Email sent to {to_email}")
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")
        raise
