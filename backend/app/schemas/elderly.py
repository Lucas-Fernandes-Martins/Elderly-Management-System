from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import date
from enum import Enum

class RiskLevelEnum(str, Enum):
    baixo = "baixo"
    medio = "medio"
    alto = "alto"

class ElderlyBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=255)
    age: int = Field(..., gt=0, lt=120)
    current_week: Optional[int] = Field(1, ge=1, le=16)
    start_date: Optional[date] = None
    risk_level: RiskLevelEnum = Field(RiskLevelEnum.baixo)
    phone: Optional[str] = Field(None, max_length=20)
    caregiver_phone: Optional[str] = Field(None, max_length=20)
    responsible_person: str = Field(..., min_length=3, max_length=255)
    health_conditions: Optional[str] = None
    observations: Optional[str] = None

class ElderlyCreate(ElderlyBase):
    pass

class ElderlyUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=255)
    age: Optional[int] = Field(None, gt=0, lt=120)
    current_week: Optional[int] = Field(None, ge=1, le=16)
    start_date: Optional[date] = None
    risk_level: Optional[RiskLevelEnum] = None
    phone: Optional[str] = Field(None, max_length=20)
    caregiver_phone: Optional[str] = Field(None, max_length=20)
    responsible_person: Optional[str] = Field(None, min_length=3, max_length=255)
    health_conditions: Optional[str] = None
    observations: Optional[str] = None

class Elderly(ElderlyBase):
    id: int
    created_at: date
    updated_at: date

    class Config:
        orm_mode = True

class ElderlyWithRecommendations(Elderly):
    recommendations: List = []

    class Config:
        orm_mode = True 