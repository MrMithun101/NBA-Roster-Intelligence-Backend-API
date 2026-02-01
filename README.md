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

## Tests

Uses pytest with an in-memory SQLite test DB (no Postgres/Redis required). FastAPI is exercised via `httpx.AsyncClient` and `ASGITransport`.

```bash
# Run all tests
pytest

# Verbose
pytest -v

# With coverage (if pytest-cov is installed)
pytest --cov=app
```

## Docker (full stack)

Run API, Postgres, and Redis with one command:

```bash
docker compose up --build
```

- **API:** http://localhost:8000 — **Docs:** http://localhost:8000/docs  
- **Postgres:** `localhost:5432` (user/pass/db from env or defaults below)  
- **Redis:** `localhost:6379`

**Container networking:** Compose creates a default network. Services reach each other by **service name** as hostname: the API uses `postgres:5432` and `redis:6379`, not `localhost`. Only the API is published on your host (port 8000); Postgres and Redis are on the same network so the API container can connect.

**Environment (optional):** Create a `.env` in the project root to override defaults:

- `POSTGRES_USER` (default: `app`)
- `POSTGRES_PASSWORD` (default: `secret`)
- `POSTGRES_DB` (default: `nba_roster_db`)

`DATABASE_URL` and `REDIS_URL` are set inside the `api` service to use hosts `postgres` and `redis`.

**One-liners:**

```bash
# Build and start all services (migrations run on API startup)
docker compose up --build

# Run in background
docker compose up -d --build

# Seed the DB after first run
docker compose run --rm api python scripts/seed.py

# Stop
docker compose down
```

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

