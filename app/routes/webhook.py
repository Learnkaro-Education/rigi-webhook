from fastapi import APIRouter, Header, HTTPException, status, Depends
from app.schemas.webhook import WebhookPayload
from app.services.webhook_service import WebhookService

router = APIRouter()

class WebhookController:
    def __init__(self, service: WebhookService):
        self.service = service

    async def handle_webhook(self, payload: WebhookPayload, apikey: str = Header(...)):
        if not self.service.verify_api_key(apikey):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API key")
        
        await self.service.process_payload(payload)
        return {"status": "success", "message": "Webhook received"}

webhook_service = WebhookService()
controller = WebhookController(webhook_service)

@router.post("")
async def webhook_entrypoint(payload: WebhookPayload, apikey: str = Header(...)):
    return await controller.handle_webhook(payload, apikey)
