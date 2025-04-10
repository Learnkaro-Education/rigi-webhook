from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

API_KEY = "a8091d5f4e66aad035ffd314df"

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
    payment_status: str  # <--- This is what you need

@app.post("/trigger-webhook")
async def receive_webhook(
    payload: WebhookPayload,
    apikey: str = Header(None)
):
    if apikey != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    payment_status = payload.payment_status

    # Now you can use it however you want:
    print(f"Received payment status: {payment_status}")

    # Optional: conditional action
    if payment_status == "failed":
        # Handle failed payment (e.g., send alert, save to DB, etc.)
        pass

    return {
        "message": "Webhook received successfully",
        "payment_status": payment_status
    }
