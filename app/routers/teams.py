"""Team endpoints: GET /teams, GET /teams/{id}, GET /teams/{id}/roster."""

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.cache import get_json, set_json
from app.db import get_db
from app.schemas import (
    RosterListResponse,
    TeamDetailResponse,
    TeamsListResponse,
)
from app.services import roster_service, team_service

router = APIRouter(prefix="/teams", tags=["teams"])

# Cache key design:
# - GET /teams: "teams:list" (no query params)
# - GET /teams/{id}/roster?season=YYYY: "teams:{team_id}:roster:{season}" so each
#   team+season combination has its own cache entry; omitting season would return
#   wrong data for different seasons.
TEAMS_LIST_KEY = "teams:list"
TEAMS_LIST_TTL = 86400  # 24h
ROSTER_TTL = 21600  # 6h


def _serialize_response(obj):
    """Pydantic v1 .dict() or v2 .model_dump()."""
    return getattr(obj, "model_dump", getattr(obj, "dict", lambda: None))()


@router.get("")
def list_teams(db: Session = Depends(get_db)):
    cached = get_json(TEAMS_LIST_KEY)
    if cached is not None:
        return JSONResponse(content=cached, headers={"X-Cache": "HIT"})
    teams = team_service.get_all_teams(db)
    response = TeamsListResponse(data=teams)
    payload = _serialize_response(response)
    set_json(TEAMS_LIST_KEY, payload, TEAMS_LIST_TTL)
    return JSONResponse(content=payload, headers={"X-Cache": "MISS"})


@router.get("/{team_id}", response_model=TeamDetailResponse)
def get_team(team_id: int, db: Session = Depends(get_db)):
    team = team_service.get_team_by_id(db, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return TeamDetailResponse(data=team)


@router.get("/{team_id}/roster")
def get_team_roster(
    team_id: int,
    season: int = Query(..., description="Season year (e.g. 2024 for 2023-24)"),
    db: Session = Depends(get_db),
):
    roster_key = f"teams:{team_id}:roster:{season}"
    cached = get_json(roster_key)
    if cached is not None:
        return JSONResponse(content=cached, headers={"X-Cache": "HIT"})
    players, team, season_obj = roster_service.get_roster_for_team_season(
        db, team_id, season
    )
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    if not season_obj:
        raise HTTPException(status_code=404, detail="Season not found")
    response = RosterListResponse(data=players, season=season, team_id=team_id)
    payload = _serialize_response(response)
    set_json(roster_key, payload, ROSTER_TTL)
    return JSONResponse(content=payload, headers={"X-Cache": "MISS"})
