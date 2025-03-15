from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import date

class ReminderBase(BaseModel):
    elderly_id: int
    scheduled_date: date
    email: str = Field(..., min_length=5, max_length=255)
    subject: str = Field(..., min_length=3, max_length=255)
    message: str = Field(..., min_length=10)

class ReminderCreate(ReminderBase):
    pass

class ReminderUpdate(BaseModel):
    scheduled_date: Optional[date] = None
    email: Optional[str] = Field(None, min_length=5, max_length=255)
    subject: Optional[str] = Field(None, min_length=3, max_length=255)
    message: Optional[str] = Field(None, min_length=10)
    sent: Optional[bool] = None
    sent_at: Optional[date] = None

class Reminder(ReminderBase):
    id: int
    sent: bool
    sent_at: Optional[date]
    created_at: date
    updated_at: date

    class Config:
        orm_mode = True 