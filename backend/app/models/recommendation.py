from sqlalchemy import Column, Integer, String, Date, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import enum
from datetime import datetime

class Category(enum.Enum):
    exercicio = "exercicio"
    alimentacao = "alimentacao"
    medicacao = "medicacao"
    social = "social"

class Adherence(enum.Enum):
    full = "full"
    partial = "partial"
    none = "none"

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    elderly_id = Column(Integer, ForeignKey("elderly.id"), nullable=False)
    week = Column(Integer, nullable=False)
    date = Column(Date, default=datetime.now().date())
    category = Column(Enum(Category), nullable=False)
    content = Column(Text, nullable=False)
    adherence = Column(Enum(Adherence))
    created_at = Column(Date, default=datetime.now().date())
    updated_at = Column(Date, default=datetime.now().date(), onupdate=datetime.now().date())

    # Relationships
    elderly = relationship("Elderly", back_populates="recommendations")
    
    def __repr__(self):
        return f"<Recommendation {self.id} for Elderly {self.elderly_id}>" 