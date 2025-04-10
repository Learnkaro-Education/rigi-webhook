from fastapi import FastAPI, Request, Header, HTTPException

app = FastAPI()

API_KEY = "a8091d5f4e66aad035ffd314df"

@app.post("/trigger-webhook")
async def trigger_webhook(request: Request, apikey: str = Header(None)):
    if apikey != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    data = await request.json()

    print("✅ Webhook received:")
    for key, value in data.items():
        print(f"{key}: {value}")

    return {
        "message": "Webhook received successfully",
        "received_fields": list(data.keys())  # just shows what fields you got
    }
