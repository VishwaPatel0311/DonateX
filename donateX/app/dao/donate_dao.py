import datetime

import paypalrestsdk

from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy import func

import settings
from models.model_donate import Donation
from schemas.schema_donate import DonationCreate

paypalrestsdk.configure({
    "mode": "sandbox",  # Use "live" for production
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})

def create_payment_intent(amount: Decimal, currency: str = "USD") -> dict:
    try:
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": f"{settings.FRONT_END_URL}/donate/success",
                "cancel_url": f"{settings.FRONT_END_URL}/donate/cancel"
            },
            "transactions": [{
                "amount": {
                    "total": str(amount),
                    "currency": currency
                },
                "description": "Donation"
            }]
        })

        if payment.create():
            for link in payment.links:
                if link.method == "REDIRECT":
                    return {
                        "approval_url": link.href,
                        "payment_id": payment.id
                    }
        raise Exception("Failed to create PayPal payment")
    except Exception as e:
        print("Error in create_payment_intent", str(e))
        raise e


def create_donation_record(
    db,
    donation: DonationCreate,
    user_id: int,
    payment_id: str,
) -> Donation:
    try:
        db_donation = Donation(
            user_id=user_id,
            amount=donation.amount,
            currency=donation.currency,
            payment_id=payment_id,
            status="pending",
        )
        db.add(db_donation)
        db.commit()
        db.refresh(db_donation)
        return db_donation
    except Exception as e:
        print("Error in create_donation_record", str(e))
        raise e


def get_donation_by_payment_id(db, payment_id):
    try:
        donation = db.query(Donation).filter(Donation.payment_id == payment_id).first()
        return donation
    except Exception as e:
        print("Error in get_donation_by_payment_id", str(e))
        raise e

def update_donation_status(db, donation):
    try:
        donation.status = "completed"
        donation.updated_at = datetime.datetime.now()
        db.commit()
    except Exception as e:
        print("Error in get_donation_by_payment_id", str(e))
        raise e

def get_donation_list_dao(db, user_id):
    try:
        result = db.query(Donation).filter(Donation.user_id == user_id)
        return result.all()
    except Exception as e:
        print("Error in get_donation_list_dao", str(e))
        raise e


def get_donation_by_id_dao(db, donation_id):
    try:
        donation = db.get(Donation, donation_id)
        return donation
    except Exception as e:
        print("Error in get_donation_by_id_dao", str(e))
        raise e

def get_donation_summary_data(db, start, end, user_id):
    try:
        data = db.query(
            func.date(Donation.created_at).label("date"),
            func.sum(Donation.amount).label("amount")
        ).filter(Donation.user_id == user_id) \
            .filter(Donation.created_at.between(start, end)) \
            .group_by(func.date(Donation.created_at)) \
            .all()

        if not data:
            raise HTTPException(status_code=404, detail="No donations found in the given range.")

        # Prepare data for plotting
        dates = [str(row.date) for row in data]
        amounts = [float(row.amount) for row in data]
        return dates, amounts
    except Exception as e:
        print("Error in get_donation_summary_data", str(e))
        raise e