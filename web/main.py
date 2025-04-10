from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta

app = FastAPI()

API_KEY = "a8091d5f4e66aad035ffd314df"

# In-memory store to prevent duplicate notifications
recent_events = {}

class WebhookPayload(BaseModel):
    Name: str
    Amount: float
    offer_code: Optional[str] = None
    offer_id: Optional[str] = None
    offer_discount: Optional[float] = None
    Email: Optional[str] = None
    Phone: Optional[str] = None
    Product: Optional[str] = None
    Link_of_Product: Optional[str] = None
    Time: Optional[str] = None
    ref_id: str
    event_type: str
    payment_status: str

@app.post("/trigger-webhook")
async def receive_webhook(
    payload: WebhookPayload,
    apikey: str = Header(None)
):
    if apikey != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    email_or_phone = payload.Email or payload.Phone
    payment_status = payload.payment_status
    current_time = datetime.utcnow()

    # Deduplication key
    key = f"{email_or_phone}_{payment_status}"

    # Remove old entries (older than 30 minutes)
    for k in list(recent_events):
        if (current_time - recent_events[k]).total_seconds() > 1800:
            del recent_events[k]

    # Check for duplicates
    if key in recent_events:
        return {
            "message": f"Ignored duplicate {payment_status} event for {email_or_phone}"
        }

    # Save the current event
    recent_events[key] = current_time

    print(f"✅ Received {payment_status} for {email_or_phone}")

    # You can add conditional logic here
    if payment_status in ["failed", "initiated"]:
        # Send alert, Telegram message, etc.
        print(f"⚠️ Payment {payment_status} — Consider notifying the user.")

    return {
        "message": "Webhook received successfully",
        "payment_status": payment_status
    }
