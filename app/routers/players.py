"""Player endpoints: GET /players with filters and pagination."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas import PaginatedPlayersResponse
from app.services import player_service

router = APIRouter(prefix="/players", tags=["players"])

DEFAULT_LIMIT = 20
MAX_LIMIT = 100


@router.get("", response_model=PaginatedPlayersResponse)
def list_players(
    team_id: int | None = Query(None, description="Filter by team (players on this team)"),
    position: str | None = Query(None, description="Filter by position (e.g. PG, SG)"),
    name: str | None = Query(None, description="Search first/last name"),
    limit: int = Query(DEFAULT_LIMIT, ge=1, le=MAX_LIMIT),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    players, total = player_service.get_players(
        db,
        team_id=team_id,
        position=position,
        name=name,
        limit=limit,
        offset=offset,
    )
    return PaginatedPlayersResponse(data=players, total=total, limit=limit, offset=offset)
