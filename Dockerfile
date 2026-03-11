# Production-style image: slim base, single stage, non-root when possible.
FROM python:3.12-slim

# Prefer stdout/stderr unbuffered so logs show up in docker compose
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install deps first so layer is cached when only app code changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application code (scripts + data for seeding)
COPY alembic.ini .
COPY alembic ./alembic
COPY app ./app
COPY scripts ./scripts
COPY data ./data

# Run as non-root (optional but good practice)
RUN adduser --disabled-password --gecos "" appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Migrations run at startup so DB is ready; then start the API
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
