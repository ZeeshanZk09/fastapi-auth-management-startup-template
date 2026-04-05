import asyncio
import logging
import smtplib
from email.message import EmailMessage

from app.config import settings

logger = logging.getLogger(__name__)


def _build_message(recipient: str, subject: str, body: str) -> EmailMessage:
    message = EmailMessage()
    message["From"] = settings.SMTP_FROM_EMAIL
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)
    return message


def _send_message_sync(message: EmailMessage) -> None:
    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=10) as smtp:
        if settings.SMTP_USE_TLS:
            smtp.starttls()
        if settings.SMTP_USERNAME and settings.SMTP_PASSWORD:
            smtp.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        smtp.send_message(message)


async def _send_email(recipient: str, subject: str, body: str) -> None:
    if not settings.EMAIL_DELIVERY_ENABLED:
        logger.info("Email delivery disabled; prepared email for %s", recipient)
        return

    message = _build_message(recipient, subject, body)
    await asyncio.to_thread(_send_message_sync, message)


async def send_verification_email(email: str, otp: str) -> None:
    await _send_email(
        recipient=email,
        subject="Verify your email",
        body=f"Your verification code is: {otp}",
    )


async def send_password_reset_email(email: str, otp: str) -> None:
    await _send_email(
        recipient=email,
        subject="Reset your password",
        body=f"Your password reset code is: {otp}",
    )
