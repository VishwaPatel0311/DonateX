import datetime

from sqlalchemy import Column, Integer, Numeric, String, DateTime, ForeignKey

from db import Base


class Donation(Base):
    __tablename__ = "donation"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(50), default="USD")
    payment_id = Column(String(100), unique=True)
    status = Column(String(50), default="pending")
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.now())
    updated_at = Column(DateTime(timezone=True), default=datetime.datetime.now())

