"""
Isolated client for fetching NBA data from nba_api (uses NBA.com public endpoints).
No API key required. If the API is down or rate-limited, raises an error so we exit cleanly.
"""

from typing import Any


def _safe_call(fn, *args, **kwargs) -> Any:
    """Call fn; if it fails, raise a clear error so sync exits without corrupting DB."""
    try:
        return fn(*args, **kwargs)
    except Exception as e:
        raise RuntimeError(f"NBA API error (API may be down): {e}") from e


def fetch_teams() -> list[dict]:
    """Fetch all NBA teams. Returns [{"id": str, "name": str, "abbreviation": str}, ...]."""
    from nba_api.stats.static import teams as nba_teams

    raw = _safe_call(nba_teams.get_teams)
    return [
        {
            "id": str(t["id"]),
            "name": t["full_name"],
            "abbreviation": t["abbreviation"],
        }
        for t in raw
    ]


def fetch_players() -> list[dict]:
    """Fetch all NBA players. Returns [{"id": str, "first_name": str, "last_name": str}, ...].
    Position is filled later from roster data."""
    from nba_api.stats.static import players as nba_players

    raw = _safe_call(nba_players.get_players)
    return [
        {
            "id": str(p["id"]),
            "first_name": p["first_name"] or "",
            "last_name": p["last_name"] or "",
        }
        for p in raw
        if p.get("first_name") or p.get("last_name")
    ]


def fetch_roster(team_id: str, season: str) -> list[dict]:
    """Fetch roster for a team in a season. season format: "2024-25".
    Returns [{"player_id": str, "position": str}, ...]."""
    from nba_api.stats.endpoints import commonteamroster

    roster = _safe_call(
        commonteamroster.CommonTeamRoster,
        team_id=int(team_id),
        season=season,
    )
    df = roster.get_data_frames()[0] if roster.get_data_frames() else None
    if df is None or df.empty:
        return []
    rows = []
    for _, row in df.iterrows():
        rows.append(
            {
                "player_id": str(row.get("PLAYER_ID", "")),
                "position": str(row.get("POSITION", "F")).strip() or "F",
            }
        )
    return rows
