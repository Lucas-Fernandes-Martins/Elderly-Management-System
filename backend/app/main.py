from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import elderly, recommendations, reminders
from app.database import engine, Base
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Elderly Care API",
    description="API for the elderly care management application",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(elderly.router, prefix="/api/elderly", tags=["elderly"])
app.include_router(recommendations.router, prefix="/api/recommendations", tags=["recommendations"])
app.include_router(reminders.router, prefix="/api/reminders", tags=["reminders"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Elderly Care API!"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"} 