from sqlalchemy import Column, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class RigiPayment(Base):
    __tablename__ = "rigi_payments"

    ref_id = Column(String, primary_key=True)
    event_type = Column(String)
    Name = Column(String)
    Amount = Column(Float)
    offer_code = Column(String)
    offer_id = Column(String)
    offer_discount = Column(Float, nullable=True)
    Email = Column(String)
    Phone = Column(String)
    Product = Column(String)
    Link_of_Product = Column(Text)
    Time = Column(String)
    payment_status = Column(String)