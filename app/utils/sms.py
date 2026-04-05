import logging

import httpx

from app.config import settings

logger = logging.getLogger(__name__)


async def send_sms_otp(phone: str, otp: str) -> None:
    if not settings.SMS_DELIVERY_ENABLED:
        logger.info("SMS delivery disabled; prepared OTP for %s", phone)
        return

    if not all([
        settings.TWILIO_ACCOUNT_SID,
        settings.TWILIO_AUTH_TOKEN,
        settings.TWILIO_FROM_NUMBER,
    ]):
        raise RuntimeError("Twilio settings are required when SMS delivery is enabled")

    url = f"https://api.twilio.com/2010-04-01/Accounts/{settings.TWILIO_ACCOUNT_SID}/Messages.json"
    payload = {
        "To": phone,
        "From": settings.TWILIO_FROM_NUMBER,
        "Body": f"Your verification code is: {otp}",
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(
            url,
            data=payload,
            auth=(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN),
        )
    response.raise_for_status()
