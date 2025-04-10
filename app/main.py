from fastapi import FastAPI, Request, Header, HTTPException
import psycopg2
import json
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
API_KEY = "a8091d5f4e66aad035ffd314df"

# PostgreSQL connection config
DB_CONFIG = {
    "dbname": "rigi_payments",
    "user": "postgres",
    "password": "root",
    "host": "localhost",
    "port": "5432"
}

def insert_payment(data):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    insert_query = """
        INSERT INTO rigi_payment (
            ref_id, event_type, Name, Amount, offer_code, offer_id, offer_discount,
            Email, Phone, Product, Link_of_Product, Time, payment_status
        ) VALUES (
            %(ref_id)s, %(event_type)s, %(Name)s, %(Amount)s, %(offer_code)s, %(offer_id)s, %(offer_discount)s,
            %(Email)s, %(Phone)s, %(Product)s, %(Link_of_Product)s, %(Time)s, %(payment_status)s
        )
        ON CONFLICT (ref_id) DO UPDATE SET
            event_type = EXCLUDED.event_type,
            Name = EXCLUDED.Name,
            Amount = EXCLUDED.Amount,
            offer_code = EXCLUDED.offer_code,
            offer_id = EXCLUDED.offer_id,
            offer_discount = EXCLUDED.offer_discount,
            Email = EXCLUDED.Email,
            Phone = EXCLUDED.Phone,
            Product = EXCLUDED.Product,
            Link_of_Product = EXCLUDED.Link_of_Product,
            Time = EXCLUDED.Time,
            payment_status = EXCLUDED.payment_status;
    """

    cur.execute(insert_query, {
        "ref_id": data.get("ref_id"),
        "event_type": data.get("event_type"),
        "Name": data.get("Name"),
        "Amount": data.get("Amount"),
        "offer_code": data.get("offer_code"),
        "offer_id": data.get("offer_id"),
        "offer_discount": data.get("offer_discount"),
        "Email": data.get("Email"),
        "Phone": data.get("Phone"),
        "Product": data.get("Product"),
        "Link_of_Product": data.get("Link of Product"),
        "Time": data.get("Time"),
        "payment_status": data.get("payment_status")
    })

    conn.commit()
    cur.close()
    conn.close()

@app.post("/trigger-webhook")
async def trigger_webhook(request: Request, apikey: str = Header(None)):
    if apikey != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    try:
        body = await request.body()
        decoded_body = body.decode()
        logger.info("🔹 Raw Body Received:\n%s", decoded_body)

        data = json.loads(decoded_body)
        logger.info("🔸 Parsed JSON Data:")
        for key, value in data.items():
            logger.info("   %s: %s", key, value)

        insert_payment(data)

        return {
            "message": "Webhook received and data saved",
            "ref_id": data.get("ref_id"),
            "payment_status": data.get("payment_status")
        }

    except json.JSONDecodeError:
        logger.error("❌ Invalid JSON received")
        raise HTTPException(status_code=400, detail="Invalid JSON payload")
