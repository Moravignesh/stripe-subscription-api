from pydantic import BaseModel


class CheckoutRequest(BaseModel):

    email: str
    plan: str