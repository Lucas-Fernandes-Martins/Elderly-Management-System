from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Recommendation as RecommendationModel, Elderly as ElderlyModel
from app.schemas import RecommendationCreate, Recommendation, RecommendationUpdate, RecommendationAdherenceUpdate
import logging
from datetime import date

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", response_model=Recommendation, status_code=status.HTTP_201_CREATED)
def create_recommendation(recommendation: RecommendationCreate, db: Session = Depends(get_db)):
    """
    Create a new recommendation for an elderly person
    """
    # Check if elderly exists
    elderly = db.query(ElderlyModel).filter(ElderlyModel.id == recommendation.elderly_id).first()
    if not elderly:
        raise HTTPException(status_code=404, detail="Elderly person not found")
    
    # Create recommendation
    db_recommendation = RecommendationModel(
        elderly_id=recommendation.elderly_id,
        week=recommendation.week,
        date=recommendation.date or date.today(),
        category=recommendation.category,
        content=recommendation.content,
        adherence=recommendation.adherence
    )
    db.add(db_recommendation)
    db.commit()
    db.refresh(db_recommendation)
    logger.info(f"Created recommendation for elderly ID {recommendation.elderly_id}")
    return db_recommendation

@router.get("/", response_model=List[Recommendation])
def read_recommendations(
    elderly_id: int = None, 
    week: int = None,
    category: str = None,
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """
    Get a list of recommendations with optional filtering
    """
    query = db.query(RecommendationModel)
    
    # Apply filters if provided
    if elderly_id:
        query = query.filter(RecommendationModel.elderly_id == elderly_id)
    if week:
        query = query.filter(RecommendationModel.week == week)
    if category:
        query = query.filter(RecommendationModel.category == category)
    
    recommendations = query.offset(skip).limit(limit).all()
    return recommendations

@router.get("/{recommendation_id}", response_model=Recommendation)
def read_recommendation(recommendation_id: int, db: Session = Depends(get_db)):
    """
    Get a recommendation by ID
    """
    recommendation = db.query(RecommendationModel).filter(RecommendationModel.id == recommendation_id).first()
    if not recommendation:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    return recommendation

@router.put("/{recommendation_id}", response_model=Recommendation)
def update_recommendation(recommendation_id: int, recommendation: RecommendationUpdate, db: Session = Depends(get_db)):
    """
    Update a recommendation
    """
    db_recommendation = db.query(RecommendationModel).filter(RecommendationModel.id == recommendation_id).first()
    if not db_recommendation:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    
    # Update fields that are provided
    for field, value in recommendation.dict(exclude_unset=True).items():
        setattr(db_recommendation, field, value)
    
    db.commit()
    db.refresh(db_recommendation)
    logger.info(f"Updated recommendation ID {recommendation_id}")
    return db_recommendation

@router.patch("/{recommendation_id}/adherence", response_model=Recommendation)
def update_recommendation_adherence(
    recommendation_id: int, 
    adherence_update: RecommendationAdherenceUpdate, 
    db: Session = Depends(get_db)
):
    """
    Update only the adherence status of a recommendation
    """
    db_recommendation = db.query(RecommendationModel).filter(RecommendationModel.id == recommendation_id).first()
    if not db_recommendation:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    
    db_recommendation.adherence = adherence_update.adherence
    db.commit()
    db.refresh(db_recommendation)
    logger.info(f"Updated adherence for recommendation ID {recommendation_id} to {adherence_update.adherence}")
    return db_recommendation

@router.delete("/{recommendation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recommendation(recommendation_id: int, db: Session = Depends(get_db)):
    """
    Delete a recommendation
    """
    db_recommendation = db.query(RecommendationModel).filter(RecommendationModel.id == recommendation_id).first()
    if not db_recommendation:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    
    db.delete(db_recommendation)
    db.commit()
    logger.info(f"Deleted recommendation ID {recommendation_id}")
    return None 