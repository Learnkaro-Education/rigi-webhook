from sqlalchemy.orm import Session
from app.schemas.webhook import WebhookPayload
from app.models.webhook_event import WebhookEvent
from app.database import SessionLocal

class WebhookService:
    def verify_api_key(self, apikey: str) -> bool:
        return apikey == "YOUR_API_KEY"

    async def process_payload(self, payload: WebhookPayload):
        db: Session = SessionLocal()
        try:
            event = WebhookEvent(
                ref_id=payload.ref_id,
                name=payload.Name,
                amount=payload.Amount,
                offer_code=payload.offer_code,
                offer_id=payload.offer_id,
                offer_discount=payload.offer_discount,
                email=payload.Email,
                phone=payload.Phone,
                product=payload.Product,
                link_of_product=payload.Link_of_Product,
                time=payload.Time,
                event_type=payload.event_type,
                payment_status=payload.payment_status,
            )
            db.add(event)
            db.commit()
        except Exception as e:
            db.rollback()
            print("Error saving webhook data:", e)
        finally:
            db.close()
