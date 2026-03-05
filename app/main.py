from fastapi import FastAPI

from app.database import Base, engine

from app.routes import plan_routes
from app.routes import payment_routes
from app.routes import webhook_routes
from app.routes import payment_routes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Stripe Subscription API")


app.include_router(plan_routes.router)

app.include_router(payment_routes.router)

app.include_router(webhook_routes.router)

app.include_router(payment_routes.router)

app.include_router(payment_routes.router)