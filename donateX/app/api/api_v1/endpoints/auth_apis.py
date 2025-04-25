from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.deps import get_db
from core import create_error_response, create_response
from dao import generate_otp, store_otp, verify_otp_dao, validate_otp
from descriptions import *
from schemas.schema_auth import PhoneRequest, OTPVerify

auth_router = APIRouter(prefix='/auth', tags=["Auth APIs"])

@auth_router.post("/request-otp",
                          name="Generates otp",
                          description=GENERATE_OTP)
def request_otp(data: PhoneRequest, db: Session = Depends(get_db)):
    try:
        otp = generate_otp()
        store_otp(db, data.phone, otp)
        print(f"DEBUG OTP for {data.phone}: {otp}")
        return create_response({"data": "OTP sent to your phone number"})
    except Exception as e:
        print(f"Exception occurred in request_otp: {str(e)}")
        return create_error_response(error=100, msg=str(e))


@auth_router.post("/verify-otp", name="Verifies Otp", description=VERIFY_OTP)
def verify_otp(data: OTPVerify, db: Session = Depends(get_db)):
    try:
        if not validate_otp(db, data.phone, data.otp):
            raise HTTPException(status_code=400, detail="Invalid or expired OTP")
        response = verify_otp_dao(db, data)
        return create_response(response)
    except Exception as e:
        print(f"Exception occurred in verify_otp: {str(e)}")
        return create_error_response(error=100, msg=str(e))


