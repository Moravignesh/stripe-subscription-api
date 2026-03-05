from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.database import Base


class Payment(Base):

    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String, index=True)

    plan = Column(String)

    amount = Column(Float)

    status = Column(String)

    transaction_id = Column(String)

    payment_date = Column(DateTime, default=datetime.utcnow)