# Job Tracker API

A REST API for managing job applications. Built with FastAPI, PostgreSQL, SQLAlchemy and Alembic.

## Features

- Create job applications
- Retrieve all applications
- Retrieve one application by ID
- Filter applications by status
- Update application status
- Delete applications
- Validate request data
- Store data persistently in PostgreSQL
- Manage database changes with Alembic
- Test endpoints with an isolated test database

## Technology Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pydantic
- pytest

## Project Structure

```text
job-tracker-api/
├── alembic/
├── database.py
├── main.py
├── models.py
├── schemas.py
├── test_main.py
├── requirements.txt
├── alembic.ini
└── .env.example
```

## Setup

Clone the repository:

```bash
git clone https://github.com/timoty-a/job-tracker-api.git
cd job-tracker-api
```

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Create the PostgreSQL database and user, then copy the environment template:

```bash
cp .env.example .env
```

Update `.env` with the correct database password:

```env
DATABASE_URL=postgresql+psycopg://job_tracker_user:your_password@localhost:5432/job_tracker_db
```

Apply database migrations:

```bash
alembic upgrade head
```

Start the development server:

```bash
fastapi dev main.py
```

Open the interactive documentation:

```text
http://127.0.0.1:8000/docs
```

## Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Check API status |
| GET | `/applications` | Retrieve all applications |
| GET | `/applications?status=interview` | Filter by status |
| GET | `/applications/{application_id}` | Retrieve one application |
| POST | `/applications` | Create an application |
| PATCH | `/applications/{application_id}` | Update an application |
| DELETE | `/applications/{application_id}` | Delete an application |

## Example Request

```json
{
  "company": "Paystack",
  "role": "Backend Engineering Intern",
  "status": "applied",
  "date_applied": "2026-08-25"
}
```

Supported statuses:

```text
applied
interview
offer
rejected
withdrawn
```

## Tests

Run the automated test suite:

```bash
python -m pytest -v
```

Tests use an isolated in-memory database and do not modify development data.