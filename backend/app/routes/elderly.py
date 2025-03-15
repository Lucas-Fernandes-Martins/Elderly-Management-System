from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Elderly as ElderlyModel
from app.schemas import ElderlyCreate, Elderly, ElderlyUpdate, ElderlyWithRecommendations
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", response_model=Elderly, status_code=status.HTTP_201_CREATED)
def create_elderly(elderly: ElderlyCreate, db: Session = Depends(get_db)):
    """
    Create a new elderly person
    """
    db_elderly = ElderlyModel(
        name=elderly.name,
        age=elderly.age,
        current_week=elderly.current_week,
        start_date=elderly.start_date,
        risk_level=elderly.risk_level,
        phone=elderly.phone,
        caregiver_phone=elderly.caregiver_phone,
        responsible_person=elderly.responsible_person,
        health_conditions=elderly.health_conditions,
        observations=elderly.observations
    )
    db.add(db_elderly)
    db.commit()
    db.refresh(db_elderly)
    logger.info(f"Created elderly person: {db_elderly.name}")
    return db_elderly

@router.get("/", response_model=List[Elderly])
def read_elderly_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get a list of elderly people
    """
    elderly_list = db.query(ElderlyModel).offset(skip).limit(limit).all()
    return elderly_list

@router.get("/{elderly_id}", response_model=ElderlyWithRecommendations)
def read_elderly(elderly_id: int, db: Session = Depends(get_db)):
    """
    Get an elderly person by ID with their recommendations
    """
    elderly = db.query(ElderlyModel).filter(ElderlyModel.id == elderly_id).first()
    if not elderly:
        raise HTTPException(status_code=404, detail="Elderly person not found")
    return elderly

@router.put("/{elderly_id}", response_model=Elderly)
def update_elderly(elderly_id: int, elderly: ElderlyUpdate, db: Session = Depends(get_db)):
    """
    Update an elderly person
    """
    db_elderly = db.query(ElderlyModel).filter(ElderlyModel.id == elderly_id).first()
    if not db_elderly:
        raise HTTPException(status_code=404, detail="Elderly person not found")
    
    # Update fields that are provided
    for field, value in elderly.dict(exclude_unset=True).items():
        setattr(db_elderly, field, value)
    
    db.commit()
    db.refresh(db_elderly)
    logger.info(f"Updated elderly person: {db_elderly.name}")
    return db_elderly

@router.delete("/{elderly_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_elderly(elderly_id: int, db: Session = Depends(get_db)):
    """
    Delete an elderly person
    """
    db_elderly = db.query(ElderlyModel).filter(ElderlyModel.id == elderly_id).first()
    if not db_elderly:
        raise HTTPException(status_code=404, detail="Elderly person not found")
    
    db.delete(db_elderly)
    db.commit()
    logger.info(f"Deleted elderly person with ID: {elderly_id}")
    return None 