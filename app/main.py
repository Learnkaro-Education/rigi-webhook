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
