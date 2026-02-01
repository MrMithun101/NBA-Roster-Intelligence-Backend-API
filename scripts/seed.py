#!/usr/bin/env python3
"""
Idempotent seed script: loads data/*.json and upserts into Postgres.

Run from project root: python scripts/seed.py (or python -m scripts.seed)

Avoiding duplicates:
- Team: get-or-create by abbreviation (unique in DB).
- Player: get-or-create by (first_name, last_name); no DB unique, so we look up first.
- Season: get-or-create by year (unique in DB).
- RosterMembership: get-or-create by (team_id, player_id, season_id) (unique in DB).

Running the script twice leaves the same row counts; no duplicate teams, players,
seasons, or roster rows.
"""

import json
import sys
from pathlib import Path

# Run from project root so "app" is importable
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv

load_dotenv(ROOT / ".env")

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models import Player, RosterMembership, Season, Team


def load_json(name: str) -> list:
    path = ROOT / "data" / name
    if not path.exists():
        raise FileNotFoundError(f"Missing data file: {path}")
    with path.open() as f:
        return json.load(f)


def get_or_create_team(session: Session, name: str, abbreviation: str) -> Team:
    stmt = select(Team).where(Team.abbreviation == abbreviation)
    team = session.execute(stmt).scalar_one_or_none()
    if team:
        return team
    team = Team(name=name, abbreviation=abbreviation)
    session.add(team)
    session.flush()  # so team.id is set
    return team


def get_or_create_player(
    session: Session, first_name: str, last_name: str, position: str
) -> Player:
    stmt = select(Player).where(
        Player.first_name == first_name, Player.last_name == last_name
    )
    player = session.execute(stmt).scalar_one_or_none()
    if player:
        return player
    player = Player(first_name=first_name, last_name=last_name, position=position)
    session.add(player)
    session.flush()
    return player


def get_or_create_season(session: Session, year: int) -> Season:
    stmt = select(Season).where(Season.year == year)
    season = session.execute(stmt).scalar_one_or_none()
    if season:
        return season
    season = Season(year=year)
    session.add(season)
    session.flush()
    return season


def get_or_create_roster(
    session: Session, team_id: int, player_id: int, season_id: int
) -> RosterMembership:
    stmt = select(RosterMembership).where(
        RosterMembership.team_id == team_id,
        RosterMembership.player_id == player_id,
        RosterMembership.season_id == season_id,
    )
    existing = session.execute(stmt).scalar_one_or_none()
    if existing:
        return existing
    rm = RosterMembership(team_id=team_id, player_id=player_id, season_id=season_id)
    session.add(rm)
    session.flush()
    return rm


def main() -> None:
    teams_data = load_json("teams.json")
    players_data = load_json("players.json")
    seasons_data = load_json("seasons.json")
    rosters_data = load_json("rosters.json")

    db = SessionLocal()
    try:
        # Teams (key: abbreviation)
        for row in teams_data:
            get_or_create_team(db, row["name"], row["abbreviation"])
        print(f"Teams: {len(teams_data)} rows (get-or-create by abbreviation)")

        # Players (key: first_name + last_name)
        for row in players_data:
            get_or_create_player(
                db, row["first_name"], row["last_name"], row["position"]
            )
        print(f"Players: {len(players_data)} rows (get-or-create by name)")

        # Seasons (key: year)
        for year in seasons_data:
            get_or_create_season(db, year)
        print(f"Seasons: {len(seasons_data)} rows (get-or-create by year)")

        # Rosters (key: team_id, player_id, season_id)
        skipped = 0
        for row in rosters_data:
            team = db.execute(
                select(Team).where(Team.abbreviation == row["team_abbreviation"])
            ).scalar_one_or_none()
            player = db.execute(
                select(Player).where(
                    Player.first_name == row["first_name"],
                    Player.last_name == row["last_name"],
                )
            ).scalar_one_or_none()
            season = db.execute(
                select(Season).where(Season.year == row["season_year"])
            ).scalar_one_or_none()
            if not team or not player or not season:
                skipped += 1
                continue
            get_or_create_roster(db, team.id, player.id, season.id)
        print(
            f"Roster memberships: {len(rosters_data) - skipped} processed, {skipped} skipped (missing team/player/season)"
        )

        db.commit()
        print("Seed complete. Run again to verify idempotency (same row counts).")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
