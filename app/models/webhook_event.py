from sqlalchemy import Column, String, Float, Text
from app.database import Base

class WebhookEvent(Base):
    __tablename__ = "webhook_events"

    ref_id = Column(String, primary_key=True, index=True)
    name = Column(String)
    amount = Column(Float)
    offer_code = Column(String, nullable=True)
    offer_id = Column(String, nullable=True)
    offer_discount = Column(String, nullable=True)
    email = Column(String)
    phone = Column(String)
    product = Column(String)
    link_of_product = Column(Text)
    time = Column(String)
    event_type = Column(String)
    payment_status = Column(String)
