"""
Pydantic schemas for API request/response validation.

Use *Response schemas as response_model in FastAPI so ORM objects are serialized
correctly (Config.from_attributes = True).
"""

from typing import Optional

from pydantic import BaseModel


# ---- Team ----
class TeamBase(BaseModel):
    name: str
    abbreviation: str


class TeamCreate(TeamBase):
    pass


class TeamResponse(TeamBase):
    id: int

    class Config:
        from_attributes = True


# ---- Player ----
class PlayerBase(BaseModel):
    first_name: str
    last_name: str
    position: str


class PlayerCreate(PlayerBase):
    pass


class PlayerResponse(PlayerBase):
    id: int

    class Config:
        from_attributes = True


# ---- Season ----
class SeasonBase(BaseModel):
    year: int


class SeasonCreate(SeasonBase):
    pass


class SeasonResponse(SeasonBase):
    id: int

    class Config:
        from_attributes = True


# ---- RosterMembership ----
class RosterMembershipBase(BaseModel):
    team_id: int
    player_id: int
    season_id: int


class RosterMembershipCreate(RosterMembershipBase):
    pass


class RosterMembershipResponse(RosterMembershipBase):
    id: int

    class Config:
        from_attributes = True


class RosterMembershipDetail(RosterMembershipResponse):
    """Roster membership with nested team, player, and season (for detail endpoints)."""
    team: Optional[TeamResponse] = None
    player: Optional[PlayerResponse] = None
    season: Optional[SeasonResponse] = None


# ---- Consistent API response wrappers ----
class TeamsListResponse(BaseModel):
    """GET /teams: list of teams."""
    data: list[TeamResponse]


class TeamDetailResponse(BaseModel):
    """GET /teams/{id}: single team."""
    data: TeamResponse


class PaginatedPlayersResponse(BaseModel):
    """GET /players: paginated list with total/limit/offset."""
    data: list[PlayerResponse]
    total: int
    limit: int
    offset: int


class RosterListResponse(BaseModel):
    """GET /teams/{id}/roster?season=: roster (players) for team in season."""
    data: list[PlayerResponse]
    season: int
    team_id: int
