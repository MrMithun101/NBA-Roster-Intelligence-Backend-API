"""
Database configuration and session management.

Sets up SQLAlchemy connection to PostgreSQL and provides database sessions
for use throughout the application.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get database connection string from environment
# Format: postgresql://username:password@host:port/database_name
DATABASE_URL = os.getenv("DATABASE_URL")

# Validate that DATABASE_URL is set
if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL environment variable is not set. "
        "Please create a .env file (copy from .env.example) and set your DATABASE_URL."
    )

# Create SQLAlchemy engine - manages connection pool to PostgreSQL
engine = create_engine(DATABASE_URL)

# Factory for creating database sessions
# autocommit=False: manual commit control
# autoflush=False: manual flush control
# bind=engine: use this engine for connections
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all database models
# All models (Player, Team, etc.) will inherit from this
Base = declarative_base()


def get_db():
    """
    Dependency function for FastAPI endpoints to get a database session.
    
    Used with Depends() to automatically provide and clean up database sessions.
    FastAPI calls this before your endpoint runs and closes the session after.
    
    Example:
        @app.get("/players")
        async def get_players(db: Session = Depends(get_db)):
            return db.query(Player).all()
    """
    # Create new session
    db = SessionLocal()
    try:
        # Yield session to endpoint (pauses here, resumes after endpoint finishes)
        yield db
    finally:
        # Always close session, even if endpoint raises an error
        db.close()

