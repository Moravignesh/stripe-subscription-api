# Stripe Subscription Payment API (FastAPI)

## Project Overview

This project is a simple **FastAPI backend service** that integrates with **Stripe Checkout** to allow users to purchase subscription plans. The system supports plan selection, payment creation using Stripe, webhook-based payment confirmation, and viewing payment history.

The application demonstrates how to integrate **Stripe payment processing with a FastAPI REST API**.

---

# Features

* List available subscription plans
* Create Stripe checkout sessions
* Redirect users to Stripe hosted payment page
* Handle Stripe webhook events
* Store payment records in database
* Retrieve payment history for a user

---

# Tech Stack

* **Backend Framework:** FastAPI
* **Database:** SQLite
* **ORM:** SQLAlchemy
* **Payment Gateway:** Stripe API
* **Environment Variables:** python-dotenv
* **Server:** Uvicorn

---

# Subscription Plans

| Plan       | Price | Billing |
| ---------- | ----- | ------- |
| Basic      | $10   | Monthly |
| Pro        | $25   | Monthly |
| Enterprise | $50   | Monthly |

---

# API Endpoints

## 1. Get Available Plans

GET /plans

Response Example

```
{
 "Basic": 10,
 "Pro": 25,
 "Enterprise": 50
}
```

---

## 2. Create Checkout Session

Creates a Stripe checkout session and redirects the user to the Stripe payment page.

POST /create-checkout-session

Request Body

```
{
 "email": "user@test.com",
 "plan": "Pro"
}
```

Response

```
{
 "checkout_url": "https://checkout.stripe.com/..."
}
```

---

## 3. Stripe Webhook

Handles Stripe payment confirmation events.

POST /webhook/stripe

Event handled:

```
checkout.session.completed
```

When payment is successful the webhook updates the payment status in the database.

---

## 4. Get Payment History

Returns all payments made by a specific user.

GET /payments/{email}

Example

```
GET /payments/user@test.com
```

Response Example

```
[
 {
  "email": "user@test.com",
  "plan": "Pro",
  "amount": 25,
  "status": "success",
  "transaction_id": "cs_test_123"
 }
]
```

---

# Project Structure

```
stripe_subscription_api
│
├── app
│   ├── main.py
│   ├── config.py
│   ├── database.py
│
│   ├── routes
│   │   ├── plan_routes.py
│   │   ├── payment_routes.py
│   │   └── webhook_routes.py
│
│   ├── services
│   │   └── stripe_service.py
│
│   ├── models
│   │   └── payment_model.py
│
│   ├── schemas
│   │   └── payment_schema.py
│
│   └── utils
│       └── plans.py
│
├── requirements.txt
├── .env.example
└── README.md
```

---

# Installation & Setup

## 1. Clone Repository

```
git clone <repository_url>
cd stripe_subscription_api
```

---

## 2. Create Virtual Environment

```
python -m venv venv
```

Activate environment

Windows

```
venv\Scripts\activate
```

---

## 3. Install Dependencies

```
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file using `.env.example`

Example `.env`:

```
STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_WEBHOOK_SECRET=your_webhook_secret
SUCCESS_URL=http://localhost:8000/success
CANCEL_URL=http://localhost:8000/cancel
```

---

## 5. Run the Application

```
uvicorn app.main:app --reload
```

Server will start at

```
http://127.0.0.1:8000
```

Swagger documentation

```
http://127.0.0.1:8000/docs
```

---

# Testing Stripe Webhooks

Install Stripe CLI and login

```
stripe login
```

Start webhook listener

```
stripe listen --forward-to localhost:8000/webhook/stripe
```

Copy the webhook signing secret and update `.env`.

---

# Testing Payment

1. Call API

```
POST /create-checkout-session
```

2. Copy the returned `checkout_url`

3. Open it in browser

4. Use Stripe test card

```
4242 4242 4242 4242
```

Expiry

```
12/34
```

CVC

```
123
```

After successful payment Stripe sends webhook to `/webhook/stripe`.

Verify payment history using

```
GET /payments/{email}
```

---

# Notes

* The system uses **email as the user identifier**.
* Payment status is initially stored as **pending**.
* After Stripe webhook confirmation, the status is updated to **success**.

---

# Conclusion

This project demonstrates a simple **Stripe payment integration using FastAPI**, including checkout session creation, webhook handling, and payment history retrieval.
