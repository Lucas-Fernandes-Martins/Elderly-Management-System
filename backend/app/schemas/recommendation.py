from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from enum import Enum

class CategoryEnum(str, Enum):
    exercicio = "exercicio"
    alimentacao = "alimentacao"
    medicacao = "medicacao"
    social = "social"

class AdherenceEnum(str, Enum):
    full = "full"
    partial = "partial"
    none = "none"

class RecommendationBase(BaseModel):
    elderly_id: int
    week: int = Field(..., ge=1, le=16)
    date: Optional[date] = None
    category: CategoryEnum
    content: str = Field(..., min_length=3)
    adherence: Optional[AdherenceEnum] = None

class RecommendationCreate(RecommendationBase):
    pass

class RecommendationUpdate(BaseModel):
    week: Optional[int] = Field(None, ge=1, le=16)
    date: Optional[date] = None
    category: Optional[CategoryEnum] = None
    content: Optional[str] = Field(None, min_length=3)
    adherence: Optional[AdherenceEnum] = None

class Recommendation(RecommendationBase):
    id: int
    created_at: date
    updated_at: date

    class Config:
        orm_mode = True

class RecommendationAdherenceUpdate(BaseModel):
    adherence: AdherenceEnum 