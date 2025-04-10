from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

WEBHOOK_URL = "https://webhook.dilsetrader.in/trigger-webhook"
YOUR_API_KEY = "a8091d5f4e66aad035ffd314df"

headers = {
    "apikey": YOUR_API_KEY,
    "Content-Type": "application/json"
}

# Pydantic model to validate incoming data
class WebhookPayload(BaseModel):
    Name: str
    Amount: int
    offer_code: str
    offer_id: str
    offer_discount: int | None
    Email: str
    Phone: str
    Product: str
    Link_of_Product: str
    Time: str
    ref_id: str
    event_type: str
    payment_status: str

@app.post("/send-full-webhook")
def send_full_webhook(payload: WebhookPayload):
    # Convert to dict and adjust field name for the API (since Link of Product has spaces)
    payload_dict = payload.dict()
    payload_dict["Link of Product"] = payload_dict.pop("Link_of_Product")

    response = requests.post(WEBHOOK_URL, headers=headers, json=payload_dict)

    return {
        "status_code": response.status_code,
        "response": response.json() if "application/json" in response.headers.get("Content-Type", "") else response.text
    }
