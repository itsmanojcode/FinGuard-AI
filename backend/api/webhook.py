import hmac
import hashlib
import json

from fastapi import APIRouter, Request, HTTPException

from backend.config import RAZORPAY_WEBHOOK_SECRET
from backend.database import get_db
from backend.models import WebhookEvent

from backend.services.event_processor import process_payment_failed


router = APIRouter()


def verify_signature(raw_body, signature):

    if not RAZORPAY_WEBHOOK_SECRET:
        raise ValueError("Webhook secret is not configured.")

    digest = hmac.new(
        RAZORPAY_WEBHOOK_SECRET.encode(),
        raw_body,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(digest, signature)


@router.post("/razorpay")
async def razorpay_webhook(request: Request):

    # 1. Read raw webhook body
    raw = await request.body()

    # 2. Get Razorpay signature
    signature = request.headers.get(
        "X-Razorpay-Signature",
        ""
    )

    # 3. Verify webhook signature
    if not verify_signature(raw, signature):
        raise HTTPException(
            status_code=401,
            detail="Invalid signature"
        )

    # 4. Parse JSON
    payload = json.loads(raw.decode())

    # 5. Get event information
    event_id = request.headers.get(
        "x-razorpay-event-id"
    )

    event_type = payload.get(
        "event",
        "unknown"
    )

    db = get_db()

    try:

        # 6. Duplicate event protection
        if event_id and db.query(WebhookEvent).filter_by(
            event_id=event_id
        ).first():

            return {
                "status": "duplicate_ignored"
            }

        # 7. Store webhook event
        stored_event_id = (
            event_id
            or f"no-id-{hash(raw)}"
        )

        db.add(
            WebhookEvent(
                event_id=stored_event_id,
                event_type=event_type
            )
        )

        db.commit()

        # 8. Process failed payment
        if event_type == "payment.failed":

            analysis = process_payment_failed(
                db=db,
                event_id=stored_event_id,
                payload=payload
            )

            return {
                "status": "processed",
                "event": event_type,
                "analysis": analysis
            }

        # 9. Other events
        return {
            "status": "accepted",
            "event": event_type
        }

    finally:
        db.close()