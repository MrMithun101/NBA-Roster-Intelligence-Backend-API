"""
Pytest fixtures and test DB setup.

Test database strategy: SQLite in-memory with dependency override.

- We set DATABASE_URL to sqlite:///:memory: before importing app so app.db doesn't
  require a real Postgres URL. We then override get_db with a session from a
  separate test engine (same Base, same tables via create_all) so we get
  check_same_thread=False and full control over the DB used in tests.
- Why: No Docker/Postgres needed for pytest; fast and deterministic; each test
  run gets a fresh in-memory DB; we avoid Alembic in tests and use
  Base.metadata.create_all so schema stays in sync with models.
"""
import os

# Must set before any app import so app.db doesn't raise or use real DB
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app

# Test engine: SQLite in-memory, single connection so schema and data persist
TEST_ENGINE = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=TEST_ENGINE)

# Create tables from models (no Alembic in tests)
Base.metadata.create_all(bind=TEST_ENGINE)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
    ) as ac:
        yield ac


@pytest.fixture
def db_session():
    """Session for inserting test data; commits so API can read it."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


def _clear_tables(session):
    from sqlalchemy import text
    for table in reversed(Base.metadata.sorted_tables):
        session.execute(text(f"DELETE FROM {table.name}"))
    session.commit()


@pytest.fixture
def seeded_data(db_session):
    """Clear tables, insert one team/player/season/roster; yield IDs."""
    from app.models import Player, RosterMembership, Season, Team

    _clear_tables(db_session)

    team = Team(name="Test Team", abbreviation="TT")
    db_session.add(team)
    db_session.flush()

    player = Player(first_name="Test", last_name="Player", position="PG")
    db_session.add(player)
    db_session.flush()

    season = Season(year=2024)
    db_session.add(season)
    db_session.flush()

    rm = RosterMembership(team_id=team.id, player_id=player.id, season_id=season.id)
    db_session.add(rm)
    db_session.commit()

    yield {"team_id": team.id, "player_id": player.id, "season_id": season.id, "season_year": 2024}
