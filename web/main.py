from fastapi import FastAPI
import requests

app = FastAPI()

WEBHOOK_URL = "https://webhook.dilsetrader.in/trigger-webhook"
YOUR_API_KEY = "a8091d5f4e66aad035ffd314df"

headers = {
    "apikey": YOUR_API_KEY,
    "Content-Type": "application/json"
}

@app.post("/trigger-webhook")
def trigger_webhook():
    data = {
        "event_type": "payment_failed"
    }

    response = requests.post(WEBHOOK_URL, headers=headers, json=data)

    return {
        "status_code": response.status_code,
        "response": response.json() if response.headers.get("Content-Type") == "application/json" else response.text
    }
