from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.stripe_service import refund_payment
from app.database import SessionLocal
from app.schemas.payment_schema import CheckoutRequest

from app.models.payment_model import Payment
from fastapi import APIRouter, HTTPException, Depends
from app.services.stripe_service import create_checkout_session
from app.utils.plans import PLANS

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@router.post("/create-checkout-session")
def create_payment(data: CheckoutRequest, db: Session = Depends(get_db)):

    try:

        session = create_checkout_session(data.email, data.plan)

        payment = Payment(
            email=data.email,
            plan=data.plan,
            amount=PLANS[data.plan],
            status="pending",
            transaction_id=session.id
        )

        db.add(payment)
        db.commit()

        return {"checkout_url": session.url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/payments/{email}")
def get_payments(email: str, db: Session = Depends(get_db)):

    payments = db.query(Payment).filter(Payment.email == email).all()

    return payments


@router.post("/refund/{transaction_id}")
def refund(transaction_id: str):

    db = SessionLocal()

    payment = db.query(Payment).filter(
        Payment.transaction_id == transaction_id
    ).first()

    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    try:
        refund = refund_payment(transaction_id)

        payment.status = "refunded"
        db.commit()

        return {
            "message": "Payment refunded successfully",
            "refund_id": refund.id
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))