from sqlalchemy import Column, Integer, String, DateTime

from db import Base


class OTPStore(Base):
    __tablename__ = "otp_store"
    id = Column(Integer, primary_key=True)
    phone = Column(String(15), nullable=False)
    otp = Column(String(6), nullable=False)
    expires_at = Column(DateTime, nullable=False)
