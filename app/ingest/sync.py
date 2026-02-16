"""
Sync ingested NBA data into Postgres.

Upsert logic:
- external_id: Stable identifier from the external API. We use it to find existing rows
  so we can update them instead of creating duplicates. Without external_id we would
  have to match by name/abbreviation, which can change and are not guaranteed unique.
- For each record: look up by external_id. If found → update fields and updated_at.
  If not found → insert new row.
"""

import time
from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.ingest.client import fetch_teams, fetch_players, fetch_roster
from app.models import Player, RosterMembership, Season, Team

# Seasons to sync (API format "YYYY-YY"); we map to our year (end year)
SEASONS_TO_SYNC = ["2024-25", "2023-24"]
ROSTER_FETCH_DELAY_SEC = 0.6  # avoid rate limits


def _season_to_year(season: str) -> int:
    """e.g. '2024-25' -> 2025, '2023-24' -> 2024."""
    parts = season.split("-")
    return int(parts[1]) if len(parts) == 2 else int(parts[0])


@dataclass
class SyncSummary:
    teams_inserted: int
    teams_updated: int
    players_inserted: int
    players_updated: int
    roster_inserted: int
    roster_unchanged: int

    def __str__(self) -> str:
        return (
            f"Teams: {self.teams_inserted} inserted, {self.teams_updated} updated | "
            f"Players: {self.players_inserted} inserted, {self.players_updated} updated | "
            f"Roster: {self.roster_inserted} inserted, {self.roster_unchanged} unchanged"
        )


def run_sync() -> SyncSummary:
    """
    Fetch data from NBA API, transform to our schema, and upsert.
    If the API fails, raises before any DB writes so we exit cleanly.
    """
    # 1. Fetch all data first; if API is down, we raise here and never touch DB
    teams_raw = fetch_teams()
    players_raw = fetch_players()

    # 2. Fetch rosters to get positions and team-player-season links
    rosters: list[tuple[str, str, list[dict]]] = []
    for team in teams_raw:
        for season in SEASONS_TO_SYNC:
            roster = fetch_roster(team["id"], season)
            rosters.append((team["id"], season, roster))
            time.sleep(ROSTER_FETCH_DELAY_SEC)

    # Build player_id -> position from roster (last seen wins)
    player_position: dict[str, str] = {}
    for _, _, entries in rosters:
        for e in entries:
            pid = str(e.get("player_id", ""))
            pos = (e.get("position") or "F").strip() or "F"
            if pid:
                player_position[pid] = pos

    db = SessionLocal()
    summary = SyncSummary(0, 0, 0, 0, 0, 0)
    try:
        # 3. Upsert teams by external_id
        for row in teams_raw:
            ext_id = str(row["id"])
            existing = db.execute(select(Team).where(Team.external_id == ext_id)).scalar_one_or_none()
            if existing:
                existing.name = row["name"]
                existing.abbreviation = row["abbreviation"]
                summary.teams_updated += 1
            else:
                t = Team(external_id=ext_id, name=row["name"], abbreviation=row["abbreviation"])
                db.add(t)
                summary.teams_inserted += 1
        db.flush()

        # 4. Build external_id -> team for roster lookups
        all_teams = {t.external_id: t for t in db.execute(select(Team)).scalars().all() if t.external_id}

        # 5. Upsert players by external_id
        for row in players_raw:
            ext_id = str(row["id"])
            pos = player_position.get(ext_id, "F")
            existing = db.execute(select(Player).where(Player.external_id == ext_id)).scalar_one_or_none()
            if existing:
                existing.first_name = row["first_name"] or ""
                existing.last_name = row["last_name"] or ""
                existing.position = pos
                summary.players_updated += 1
            else:
                p = Player(
                    external_id=ext_id,
                    first_name=row["first_name"] or "",
                    last_name=row["last_name"] or "",
                    position=pos,
                )
                db.add(p)
                summary.players_inserted += 1
        db.flush()

        # 6. Build external_id -> player for roster lookups
        all_players = {p.external_id: p for p in db.execute(select(Player)).scalars().all() if p.external_id}

        # 7. Get-or-create seasons
        season_by_year: dict[int, Season] = {}
        for s in SEASONS_TO_SYNC:
            year = _season_to_year(s)
            if year not in season_by_year:
                existing = db.execute(select(Season).where(Season.year == year)).scalar_one_or_none()
                if existing:
                    season_by_year[year] = existing
                else:
                    season_by_year[year] = Season(year=year)
                    db.add(season_by_year[year])
        db.flush()

        # 8. Upsert roster memberships
        for team_ext_id, season_str, entries in rosters:
            team = all_teams.get(team_ext_id)
            if not team:
                continue
            year = _season_to_year(season_str)
            season = season_by_year.get(year)
            if not season:
                continue
            for e in entries:
                player_ext_id = str(e.get("player_id", ""))
                player = all_players.get(player_ext_id)
                if not player:
                    continue
                stmt = select(RosterMembership).where(
                    RosterMembership.team_id == team.id,
                    RosterMembership.player_id == player.id,
                    RosterMembership.season_id == season.id,
                )
                if db.execute(stmt).scalar_one_or_none():
                    summary.roster_unchanged += 1
                else:
                    db.add(
                        RosterMembership(
                            team_id=team.id,
                            player_id=player.id,
                            season_id=season.id,
                        )
                    )
                    summary.roster_inserted += 1

        db.commit()
        return summary
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
