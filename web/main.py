from fastapi import FastAPI, Request, Header, HTTPException
import json

app = FastAPI()

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

        payment_status = data.get("payment_status")
        ref_id = data.get("ref_id")

        print(f"✅ Payment Status: {payment_status}")
        print(f"🆔 Ref ID: {ref_id}")

        return {
            "message": "Webhook received successfully",
            "payment_status": payment_status,
            "ref_id": ref_id
        }

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")
