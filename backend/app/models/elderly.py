from sqlalchemy import Column, Integer, String, Date, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import enum
from datetime import datetime

class RiskLevel(enum.Enum):
    baixo = "baixo"
    medio = "medio"
    alto = "alto"

class Elderly(Base):
    __tablename__ = "elderly"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    age = Column(Integer, nullable=False)
    current_week = Column(Integer, default=1)
    start_date = Column(Date, default=datetime.now().date())
    risk_level = Column(Enum(RiskLevel), default=RiskLevel.baixo)
    phone = Column(String(20))
    caregiver_phone = Column(String(20))
    responsible_person = Column(String(255), nullable=False)
    health_conditions = Column(Text)
    observations = Column(Text)
    created_at = Column(Date, default=datetime.now().date())
    updated_at = Column(Date, default=datetime.now().date(), onupdate=datetime.now().date())

    # Relationships
    recommendations = relationship("Recommendation", back_populates="elderly", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Elderly {self.name}>" 