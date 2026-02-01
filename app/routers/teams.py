"""Team endpoints: GET /teams, GET /teams/{id}, GET /teams/{id}/roster."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas import (
    RosterListResponse,
    TeamDetailResponse,
    TeamsListResponse,
)
from app.services import roster_service, team_service

router = APIRouter(prefix="/teams", tags=["teams"])


@router.get("", response_model=TeamsListResponse)
def list_teams(db: Session = Depends(get_db)):
    teams = team_service.get_all_teams(db)
    return TeamsListResponse(data=teams)


@router.get("/{team_id}", response_model=TeamDetailResponse)
def get_team(team_id: int, db: Session = Depends(get_db)):
    team = team_service.get_team_by_id(db, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return TeamDetailResponse(data=team)


@router.get("/{team_id}/roster", response_model=RosterListResponse)
def get_team_roster(
    team_id: int,
    season: int = Query(..., description="Season year (e.g. 2024 for 2023-24)"),
    db: Session = Depends(get_db),
):
    players, team, season_obj = roster_service.get_roster_for_team_season(
        db, team_id, season
    )
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    if not season_obj:
        raise HTTPException(status_code=404, detail="Season not found")
    return RosterListResponse(data=players, season=season, team_id=team_id)
