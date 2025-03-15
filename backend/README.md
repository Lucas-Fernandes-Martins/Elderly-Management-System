# Elderly Care Backend

Backend API for the Elderly Care Management System. This API allows for tracking elderly patients' weekly activities, managing schedules, and facilitating communication through automated reminders.

## Features

- Register and manage elderly individuals
- Add and track recommendations
- Monitor adherence to recommendations
- Set up automated email reminders for care providers

## Technology Stack

- FastAPI - Modern, fast web framework for building APIs
- PostgreSQL - Robust, open-source database
- SQLAlchemy - SQL toolkit and ORM
- Pydantic - Data validation and settings management

## Setup Instructions

### 1. Prerequisites

- Python 3.8+
- PostgreSQL 12+

### 2. Clone the Repository

```bash
git clone <repository-url>
cd backend
```

### 3. Set Up a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

```bash
cp .env.example .env
```

Edit the `.env` file with your database and email settings.

### 6. Set Up the Database

Create a PostgreSQL database:

```bash
createdb elderly_care
```

The tables will be auto-created when the application starts.

### 7. Run the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000.

## API Documentation

Once the server is running, you can access the interactive API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Email Reminders

To set up automated email reminders:

1. Configure your SMTP settings in the `.env` file
2. Set up a cron job or task scheduler to call the `/api/reminders/send-due` endpoint daily

Example cron job (runs at 8:00 AM every day):

```
0 8 * * * curl -X POST http://localhost:8000/api/reminders/send-due
```

## License

[MIT](LICENSE) 