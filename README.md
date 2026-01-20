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

## Running Locally

Start the development server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## Endpoints

- `GET /health` - Health check endpoint returning `{"status": "ok"}`

## Project Structure

- `app/` - Main application code
- `tests/` - Test files
- `scripts/` - Utility scripts
- `data/` - Data files

