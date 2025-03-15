from sqlalchemy import Column, Integer, String, Date, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    elderly_id = Column(Integer, ForeignKey("elderly.id"), nullable=False)
    scheduled_date = Column(Date, nullable=False)
    email = Column(String(255), nullable=False)
    subject = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    sent = Column(Boolean, default=False)
    sent_at = Column(Date)
    created_at = Column(Date, default=datetime.now().date())
    updated_at = Column(Date, default=datetime.now().date(), onupdate=datetime.now().date())

    # Relationships
    elderly = relationship("Elderly")
    
    def __repr__(self):
        return f"<Reminder {self.id} for Elderly {self.elderly_id}>" 