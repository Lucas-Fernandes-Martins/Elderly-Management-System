from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Reminder as ReminderModel, Elderly as ElderlyModel
from app.schemas import ReminderCreate, Reminder, ReminderUpdate
from app.services.email_service import email_service
import logging
from datetime import date

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", response_model=Reminder, status_code=status.HTTP_201_CREATED)
def create_reminder(reminder: ReminderCreate, db: Session = Depends(get_db)):
    """
    Create a new reminder for an elderly person
    """
    # Check if elderly exists
    elderly = db.query(ElderlyModel).filter(ElderlyModel.id == reminder.elderly_id).first()
    if not elderly:
        raise HTTPException(status_code=404, detail="Elderly person not found")
    
    # Create reminder
    db_reminder = ReminderModel(
        elderly_id=reminder.elderly_id,
        scheduled_date=reminder.scheduled_date,
        email=reminder.email,
        subject=reminder.subject,
        message=reminder.message,
        sent=False
    )
    db.add(db_reminder)
    db.commit()
    db.refresh(db_reminder)
    logger.info(f"Created reminder for elderly ID {reminder.elderly_id}")
    return db_reminder

@router.get("/", response_model=List[Reminder])
def read_reminders(
    elderly_id: int = None,
    scheduled_date: date = None,
    sent: bool = None,
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """
    Get a list of reminders with optional filtering
    """
    query = db.query(ReminderModel)
    
    # Apply filters if provided
    if elderly_id:
        query = query.filter(ReminderModel.elderly_id == elderly_id)
    if scheduled_date:
        query = query.filter(ReminderModel.scheduled_date == scheduled_date)
    if sent is not None:
        query = query.filter(ReminderModel.sent == sent)
    
    reminders = query.offset(skip).limit(limit).all()
    return reminders

@router.get("/{reminder_id}", response_model=Reminder)
def read_reminder(reminder_id: int, db: Session = Depends(get_db)):
    """
    Get a reminder by ID
    """
    reminder = db.query(ReminderModel).filter(ReminderModel.id == reminder_id).first()
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    return reminder

@router.put("/{reminder_id}", response_model=Reminder)
def update_reminder(reminder_id: int, reminder: ReminderUpdate, db: Session = Depends(get_db)):
    """
    Update a reminder
    """
    db_reminder = db.query(ReminderModel).filter(ReminderModel.id == reminder_id).first()
    if not db_reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    
    # Update fields that are provided
    for field, value in reminder.dict(exclude_unset=True).items():
        setattr(db_reminder, field, value)
    
    db.commit()
    db.refresh(db_reminder)
    logger.info(f"Updated reminder ID {reminder_id}")
    return db_reminder

@router.post("/{reminder_id}/send", response_model=Reminder)
def send_reminder(reminder_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Send a reminder by ID
    """
    db_reminder = db.query(ReminderModel).filter(ReminderModel.id == reminder_id).first()
    if not db_reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    
    if db_reminder.sent:
        raise HTTPException(status_code=400, detail="Reminder has already been sent")
    
    # Get the elderly person
    elderly = db.query(ElderlyModel).filter(ElderlyModel.id == db_reminder.elderly_id).first()
    if not elderly:
        raise HTTPException(status_code=404, detail="Elderly person not found")
    
    # Send email in the background
    background_tasks.add_task(
        send_reminder_email, 
        db_reminder.id, 
        db_reminder.email, 
        elderly.name, 
        db_reminder.subject, 
        db_reminder.message,
        db
    )
    
    return db_reminder

@router.post("/send-due", status_code=status.HTTP_200_OK)
def send_due_reminders(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Send all due reminders (scheduled for today or earlier that haven't been sent)
    """
    today = date.today()
    due_reminders = db.query(ReminderModel).filter(
        ReminderModel.scheduled_date <= today,
        ReminderModel.sent == False
    ).all()
    
    for reminder in due_reminders:
        # Get the elderly person
        elderly = db.query(ElderlyModel).filter(ElderlyModel.id == reminder.elderly_id).first()
        if elderly:
            # Send email in the background
            background_tasks.add_task(
                send_reminder_email, 
                reminder.id, 
                reminder.email, 
                elderly.name, 
                reminder.subject, 
                reminder.message,
                db
            )
    
    return {"message": f"Sending {len(due_reminders)} due reminders"}

@router.delete("/{reminder_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reminder(reminder_id: int, db: Session = Depends(get_db)):
    """
    Delete a reminder
    """
    db_reminder = db.query(ReminderModel).filter(ReminderModel.id == reminder_id).first()
    if not db_reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    
    db.delete(db_reminder)
    db.commit()
    logger.info(f"Deleted reminder ID {reminder_id}")
    return None

def send_reminder_email(reminder_id: int, to_email: str, elderly_name: str, subject: str, message: str, db: Session):
    """
    Function to send reminder emails in the background
    """
    try:
        # Send the email
        success = email_service.send_reminder(to_email, elderly_name, subject, message)
        
        # Update reminder status
        db_reminder = db.query(ReminderModel).filter(ReminderModel.id == reminder_id).first()
        if db_reminder and success:
            db_reminder.sent = True
            db_reminder.sent_at = date.today()
            db.commit()
            logger.info(f"Sent reminder ID {reminder_id} to {to_email}")
        elif not success:
            logger.error(f"Failed to send reminder ID {reminder_id} to {to_email}")
    except Exception as e:
        logger.error(f"Error sending reminder: {str(e)}") 