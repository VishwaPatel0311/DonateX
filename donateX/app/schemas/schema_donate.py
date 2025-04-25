from typing import Optional
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel

class DonationBase(BaseModel):
    amount: Decimal
    currency: str = "USD"

class DonationCreate(DonationBase):
    pass

class DonationUpdate(DonationBase):
    status: Optional[str] = None

class DonationInDB(DonationBase):
    id: int
    user_id: int
    payment_id: str
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class DonationResponse(DonationInDB):
    pass