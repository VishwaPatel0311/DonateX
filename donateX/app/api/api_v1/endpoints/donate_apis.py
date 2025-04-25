import io
from datetime import datetime
from typing import List

import paypalrestsdk
from fastapi import Depends, APIRouter, Query, HTTPException
from sqlalchemy import func
from starlette.responses import StreamingResponse, JSONResponse
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from api.deps import get_db
from core import create_response, create_error_response
from dao import get_current_user
from dao.donate_dao import create_payment_intent, create_donation_record, get_donation_list_dao, \
    get_donation_by_id_dao, get_donation_summary_data, get_donation_by_payment_id, update_donation_status
from models import Donation
from models.model_user import User
from schemas.schema_donate import DonationCreate, DonationResponse

donatex_router = APIRouter(prefix='/donate', tags=["Donate APIs"])

@donatex_router.post("/", response_model=dict)
def create_donation(
    donation: DonationCreate,
    current_user: User = Depends(get_current_user),
    db= Depends(get_db)
):
    try:
        payment_intent = create_payment_intent(donation.amount, donation.currency)
        donation_record = create_donation_record(
            db, donation, current_user["sub"], payment_intent["payment_id"]
        )
        return create_response({
            "client_secret": payment_intent["payment_id"],
            "approval_url": payment_intent["approval_url"],
            "donation_id": donation_record.id
        })
    except Exception as e:
        print(f"Exception occurred in create_donation: {str(e)}")
        return create_error_response(error=100, msg=str(e))


@donatex_router.get("/verify")
def verify_paypal_payment(payment_id: str, payer_id: str, db=Depends(get_db)):
    try:
        payment = paypalrestsdk.Payment.find(payment_id)

        if payment.execute({"payer_id": payer_id}):
            # Update donation status in DB
            donation = get_donation_by_payment_id(db, payment_id)
            if donation:
                update_donation_status(db, donation)
                return create_response({"message": "Payment verified successfully."})
            else:
                return create_error_response(error=104, msg="Donation record not found")
        else:
            return create_error_response(error=105, msg="Payment execution failed")

    except Exception as e:
        print(f"Error in verifying PayPal payment: {str(e)}")
        return create_error_response(error=100, msg="Payment verification failed")


@donatex_router.get("/list", response_model=List[DonationResponse])
def get_donation_list(
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    try:
        donations = get_donation_list_dao(db, current_user["sub"])
        donation_response = [DonationResponse.from_orm(d) for d in donations]
        return create_response(donation_response)
    except Exception as e:
        print(f"Exception occurred in get_donation_list: {str(e)}")
        return create_error_response(error=100, msg=str(e))


@donatex_router.get("/{donation_id}",response_model=DonationResponse)
def get_donation(
    donation_id: int,
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    try:
        donation = get_donation_by_id_dao(db, donation_id)
        if not donation or donation.user_id != int(current_user["sub"]):
            return create_error_response(error=103, msg="Donation not found")
        donation_response = DonationResponse.from_orm(donation)
        return create_response(donation_response)
    except Exception as e:
        print(f"Exception occurred in get_donation: {str(e)}")
        return create_error_response(error=100, msg=str(e))


@donatex_router.get("/summary/plot")
def donation_summary_plot(
    start_date: str = Query(...),
    end_date: str = Query(...),
    db = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    dates, amounts = get_donation_summary_data(db, start, end, current_user["sub"])

    # Create plot
    plt.figure(figsize=(10, 5))
    plt.plot(dates, amounts, marker='o')
    plt.title("Donation Trend")
    plt.xlabel("Date")
    plt.ylabel("Amount ($)")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save plot to a BytesIO buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)

    # Return image
    return StreamingResponse(buf, media_type="image/png")