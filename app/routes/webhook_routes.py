from fastapi import APIRouter, Request, HTTPException
import stripe

from app.config import STRIPE_WEBHOOK_SECRET
from app.database import SessionLocal
from app.models.payment_model import Payment

router = APIRouter()


@router.post("/webhook/stripe")
async def stripe_webhook(request: Request):

    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    # Prevent manual calls without Stripe signature
    if sig_header is None:
        raise HTTPException(
            status_code=400,
            detail="Missing Stripe signature header"
        )

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            STRIPE_WEBHOOK_SECRET
        )
    except stripe.error.SignatureVerificationError:
        raise HTTPException(
            status_code=400,
            detail="Invalid Stripe signature"
        )

    if event["type"] == "checkout.session.completed":

        session = event["data"]["object"]

        transaction_id = session["id"]

        db = SessionLocal()

        payment = db.query(Payment).filter(
            Payment.transaction_id == transaction_id
        ).first()

        if payment:
            payment.status = "success"
            db.commit()

        db.close()

    return {"status": "success"}