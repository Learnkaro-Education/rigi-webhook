from fastapi import FastAPI, Request, Header, HTTPException
import json
from database import SessionLocal, engine
from models import Base, RigiPayment

app = FastAPI()
Base.metadata.create_all(bind=engine)

API_KEY = "a8091d5f4e66aad035ffd314df"

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

        db = SessionLocal()
        payment = RigiPayment(
            ref_id=data.get("ref_id"),
            event_type=data.get("event_type"),
            Name=data.get("Name"),
            Amount=data.get("Amount"),
            offer_code=data.get("offer_code"),
            offer_id=data.get("offer_id"),
            offer_discount=data.get("offer_discount"),
            Email=data.get("Email"),
            Phone=data.get("Phone"),
            Product=data.get("Product"),
            Link_of_Product=data.get("Link of Product"),
            Time=data.get("Time"),
            payment_status=data.get("payment_status")
        )
        db.merge(payment)
        db.commit()
        db.close()

        return {
            "message": "Webhook received and data saved",
            "ref_id": data.get("ref_id"),
            "payment_status": data.get("payment_status")
        }

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")