import random
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from starlette import status

import settings
from models.model_otp_store import OTPStore
from models.model_user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def generate_otp():
    try:
        return str(random.randint(100000, 999999))
    except Exception as e:
        print("In generate_otp", str(e))
        raise e

def store_otp(db: Session, phone: str, otp: str):
    try:
        expires = datetime.utcnow() + timedelta(minutes=5)
        db.query(OTPStore).filter(OTPStore.phone == phone).delete()
        db.add(OTPStore(phone=phone, otp=otp, expires_at=expires))
        db.commit()
    except Exception as e:
        print("In store_otp", str(e))
        raise e

def validate_otp(db: Session, phone: str, otp: str):
    try:
        otp_entry = db.query(OTPStore).filter(OTPStore.phone == phone).first()
        if otp_entry and otp_entry.otp == otp and otp_entry.expires_at > datetime.utcnow():
            db.delete(otp_entry)
            db.commit()
            return True
        return False
    except Exception as e:
        print("In validate_otp", str(e))
        raise e


def create_access_token(data: dict):
    try:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    except Exception as e:
        print("In create_access_token", str(e))
        raise e


def verify_otp_dao(db, data):
    try:
        user = db.query(User).filter(User.phone == data.phone).first()
        if not user:
            user = User(phone=data.phone)
            db.add(user)
            db.commit()
            db.refresh(user)

        access_token = create_access_token(data={"sub": str(user.id)})
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        print("In verify_otp_dao", str(e))
        raise e

def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload is None:
            raise credentials_exception
        return payload
    except JWTError:
        raise credentials_exception