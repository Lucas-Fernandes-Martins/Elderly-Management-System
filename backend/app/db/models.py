from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DateTime, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone = Column(String)
    group = Column(String)  # GC or GI
    current_week = Column(Integer)
    
    # Relationships
    caretakers = relationship("Caretaker", back_populates="patient")
    calls = relationship("Call", back_populates="patient")
    action_plans = relationship("ActionPlan", back_populates="patient")
    reports = relationship("Report", back_populates="patient")

class Caretaker(Base):
    __tablename__ = "caretakers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone = Column(String)
    patient_id = Column(Integer, ForeignKey("patients.id"))

    # Relationships
    patient = relationship("Patient", back_populates="caretakers")

class Call(Base):
    __tablename__ = "calls"

    id = Column(Integer, primary_key=True, index=True)
    call_number = Column(Integer)  # 1-16
    week = Column(Integer)
    scheduled_date = Column(DateTime)
    completed = Column(Boolean, default=False)
    notes = Column(Text)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    
    # Relationships
    patient = relationship("Patient", back_populates="calls")
    questions = relationship("Question", back_populates="call")
    recommendations = relationship("Recommendation", back_populates="call")

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(Text)
    answer = Column(Text)
    call_id = Column(Integer, ForeignKey("calls.id"))
    
    # Relationships
    call = relationship("Call", back_populates="questions")

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text)
    call_id = Column(Integer, ForeignKey("calls.id"))
    
    # Relationships
    call = relationship("Call", back_populates="recommendations")

class ActionPlan(Base):
    __tablename__ = "action_plans"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime)
    modified_at = Column(DateTime)
    content = Column(Text)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    
    # Relationships
    patient = relationship("Patient", back_populates="action_plans")

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime)
    content = Column(Text)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    
    # Relationships
    patient = relationship("Patient", back_populates="reports")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    sent_at = Column(DateTime)
    recipient_numbers = Column(Text)  # Comma-separated list of phone numbers
    status = Column(String)  # sent, delivered, failed 