import stripe
from app.config import STRIPE_SECRET_KEY, SUCCESS_URL, CANCEL_URL
from app.utils.plans import PLANS

stripe.api_key = STRIPE_SECRET_KEY


def create_checkout_session(email, plan):

    price = PLANS.get(plan)

    session = stripe.checkout.Session.create(

        payment_method_types=["card"],

        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": f"{plan} Subscription",
                    },
                    "unit_amount": int(price * 100),
                },
                "quantity": 1,
            }
        ],

        mode="payment",

        success_url=SUCCESS_URL,

        cancel_url=CANCEL_URL,

        customer_email=email,

        metadata={
            "plan": plan
        }
    )

    return session

def refund_payment(transaction_id: str):
    refund = stripe.Refund.create(
        payment_intent=transaction_id
    )
    return refund