# NBA Roster Intelligence Backend API

A FastAPI-based backend API for NBA roster intelligence.

## Setup

1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```

2. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env and add your PostgreSQL database URL
   # Format: postgresql://username:password@localhost:5432/database_name
   ```

5. Set up the database:
   ```bash
   # Make sure PostgreSQL is running and create a database
   # Example: createdb nba_roster_db
   
   # Run database migrations
   alembic upgrade head
   ```

## Running Locally

Start the development server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## Endpoints

- `GET /health` - Health check endpoint returning `{"status": "ok"}`

## Database Migrations

Alembic is used to manage database schema changes:

```bash
# Create a new migration (after changing models)
alembic revision --autogenerate -m "description of changes"

# Apply migrations to database
alembic upgrade head

# Rollback last migration
alembic downgrade -1
```

## Project Structure

- `app/` - Main application code
  - `main.py` - FastAPI application and routes
  - `db.py` - Database configuration and session management
- `alembic/` - Database migration files
- `tests/` - Test files
- `scripts/` - Utility scripts
- `data/` - Data files

