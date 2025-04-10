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
        INSERT INTO rigi_pmts (
            ref_id, event_type, name, amount, offer_code, offer_id, offer_discount,
            email, phone, product, link_of_product, time, payment_status
        ) VALUES (
            %(ref_id)s, %(event_type)s, %(name)s, %(amount)s, %(offer_code)s, %(offer_id)s, %(offer_discount)s,
            %(email)s, %(phone)s, %(product)s, %(link_of_product)s, %(time)s, %(payment_status)s
        )
        ON CONFLICT (ref_id) DO UPDATE SET
            event_type = EXCLUDED.event_type,
            name = EXCLUDED.name,
            amount = EXCLUDED.amount,
            offer_code = EXCLUDED.offer_code,
            offer_id = EXCLUDED.offer_id,
            offer_discount = EXCLUDED.offer_discount,
            email = EXCLUDED.email,
            phone = EXCLUDED.phone,
            product = EXCLUDED.product,
            link_of_product = EXCLUDED.link_of_product,
            time = EXCLUDED.time,
            payment_status = EXCLUDED.payment_status;
    """

    cur.execute(insert_query, {
        "ref_id": data.get("ref_id"),
        "event_type": data.get("event_type"),
        "name": data.get("Name"),
        "amount": data.get("Amount"),
        "offer_code": data.get("offer_code"),
        "offer_id": data.get("offer_id"),
        "offer_discount": data.get("offer_discount"),
        "email": data.get("Email"),
        "phone": data.get("Phone"),
        "product": data.get("Product"),
        "link_of_product": data.get("Link of Product"),
        "time": data.get("Time"),
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
