from pydantic import BaseModel
from typing import Optional

class WebhookPayload(BaseModel):
    Name: str
    Amount: float  # In INR
    offer_code: Optional[str] = None
    offer_id: Optional[str] = None
    offer_discount: Optional[str] = None
    Email: str
    Phone: str
    Product: str
    Link_of_Product: str  # Adjusted for Python
    Time: str
    ref_id: str
    event_type: str
    payment_status: str  # "initiated" or "failed"
