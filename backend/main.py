from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from typing import List, Optional
from pydantic import BaseModel
from app.api.routes import patients, calls, action_plans, reports

app = FastAPI(
    title="Elderly Care Management API",
    description="API for managing elderly care and monitoring system",
    version="1.0.0"
)

# CORS configuration
origins = [
    "http://localhost:3000",  # React development server
    "http://localhost:5000",  # Production build
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class Patient(BaseModel):
    id: Optional[int] = None
    name: str
    age: int
    phone: str
    caregiver_phone: Optional[str] = None
    current_week: int
    start_date: datetime

class WeeklyCall(BaseModel):
    id: Optional[int] = None
    patient_id: int
    week_number: int
    scheduled_date: datetime
    completed: bool = False
    notes: Optional[str] = None
    recommendations: Optional[str] = None

class ActionPlan(BaseModel):
    id: Optional[int] = None
    patient_id: int
    created_at: datetime
    updated_at: datetime
    content: str
    status: str = "active"

# Routes
@app.get("/")
async def root():
    return {"message": "Elderly Care Management API"}

@app.get("/patients", response_model=List[Patient])
async def get_patients():
    # TODO: Implement database query
    return []

@app.post("/patients", response_model=Patient)
async def create_patient(patient: Patient):
    # TODO: Implement database insertion
    return patient

@app.get("/patients/{patient_id}/weekly-calls", response_model=List[WeeklyCall])
async def get_patient_calls(patient_id: int):
    # TODO: Implement database query
    return []

@app.post("/weekly-calls", response_model=WeeklyCall)
async def create_weekly_call(call: WeeklyCall):
    # TODO: Implement database insertion
    return call

@app.put("/weekly-calls/{call_id}", response_model=WeeklyCall)
async def update_weekly_call(call_id: int, call: WeeklyCall):
    # TODO: Implement database update
    return call

@app.get("/patients/{patient_id}/action-plan", response_model=ActionPlan)
async def get_patient_action_plan(patient_id: int):
    # TODO: Implement database query
    return None

@app.post("/action-plans", response_model=ActionPlan)
async def create_action_plan(plan: ActionPlan):
    # TODO: Implement database insertion
    return plan

@app.put("/action-plans/{plan_id}", response_model=ActionPlan)
async def update_action_plan(plan_id: int, plan: ActionPlan):
    # TODO: Implement database update
    return plan

# Include routers
app.include_router(patients.router, prefix="/api", tags=["patients"])
app.include_router(calls.router, prefix="/api", tags=["calls"])
app.include_router(action_plans.router, prefix="/api", tags=["action_plans"])
app.include_router(reports.router, prefix="/api", tags=["reports"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 