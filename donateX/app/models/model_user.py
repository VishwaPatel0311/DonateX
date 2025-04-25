from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean

from db import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    phone = Column(String(15), unique=True, nullable=False)
    full_name = Column(String(50), nullable=True)
    email = Column(String(50), unique=True, index=True, nullable=True)
    hashed_password = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow)