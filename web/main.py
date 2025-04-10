from fastapi import FastAPI, Request, Header, HTTPException, BackgroundTasks
import json
import time
import threading
from contextlib import contextmanager

app = FastAPI()

API_KEY = "a8091d5f4e66aad035ffd314df"
keep_logging = True  # Global flag to stop/start the logger


@contextmanager
def log_every_5_seconds():
    def log():
        while keep_logging:
            print("⏱️ Listening for Webhook")
            time.sleep(5)

    thread = threading.Thread(target=log, daemon=True)
    thread.start()
    try:
        yield
    finally:
        print("🛑 Stopped logging.")


@app.on_event("startup")
def startup_event():
    # Start background logging at startup
    global keep_logging
    keep_logging = True
    with log_every_5_seconds():
        # Allow it to run in the background
        time.sleep(0.1)


@app.post("/trigger-webhook")
async def trigger_webhook(request: Request, apikey: str = Header(None)):
    if apikey != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    try:
        body = await request.body()
        decoded_body = body.decode()
        print("🔹 Raw Body Received:")
        print(decoded_body)

        data = json.loads(decoded_body)
        print("🔸 Parsed JSON Data:")
        for key, value in data.items():
            print(f"   {key}: {value}")

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    payment_status = data.get("payment_status")
    ref_id = data.get("ref_id")

    print(f"✅ Payment Status: {payment_status}")
    print(f"🆔 Ref ID: {ref_id}")

    return {
        "message": "Webhook received successfully",
        "payment_status": payment_status,
        "ref_id": ref_id
    }
