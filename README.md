# Elderly Care Management System

A comprehensive system for managing elderly care, including weekly calls, action plans, and monitoring.

## Features

- Patient management
- Weekly call scheduling and tracking
- Action plan creation and updates
- Report generation
- SMS messaging system
- Progressive Web App (PWA) support

## Project Structure

```
.
├── frontend-magic/        # React frontend
│   ├── public/           # Static files
│   └── src/              # Source code
│       ├── components/   # Reusable components
│       ├── pages/        # Page components
│       └── services/     # API services
└── backend/              # FastAPI backend
    ├── models.py         # Database models
    ├── database.py      # Database configuration
    ├── main.py          # Main application
    └── requirements.txt  # Python dependencies
```

## Prerequisites

- Node.js >= 14
- Python >= 3.8
- PostgreSQL >= 12

## Setup

### Backend Setup

1. Create a virtual environment:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and configure your environment variables:
   ```bash
   cp .env.example .env
   ```

4. Create the database:
   ```bash
   createdb elderly_care
   ```

5. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Install dependencies:
   ```bash
   cd frontend-magic
   npm install
   ```

2. Start the development server:
   ```bash
   npm start
   ```

The application will be available at `http://localhost:3000`

## Development

### API Documentation

Once the backend is running, you can access the API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Frontend Development

The frontend is built with:
- React
- Material-UI (MUI)
- React Router
- PWA support

### Backend Development

The backend is built with:
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- Twilio (for SMS)

## Deployment

### Frontend Deployment

1. Build the production version:
   ```bash
   cd frontend-magic
   npm run build
   ```

2. The build files will be in the `build` directory, ready to be served by any static file server.

### Backend Deployment

1. Set up your production database
2. Configure your production environment variables
3. Run with a production ASGI server:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

## License

This project is licensed under the MIT License - see the LICENSE file for details. # Elderly-Management-System
