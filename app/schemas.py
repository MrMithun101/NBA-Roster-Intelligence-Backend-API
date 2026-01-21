"""
Pydantic schemas for request/response validation.

These schemas define the structure of data going in and out of the API.
They automatically validate data and convert between Python objects and JSON.
"""

from pydantic import BaseModel
from typing import Optional


# Team Schemas
class TeamBase(BaseModel):
    """Base schema for Team with common fields."""
    name: str
    abbreviation: str


class TeamCreate(TeamBase):
    """Schema for creating a new team."""
    pass


class TeamResponse(TeamBase):
    """Schema for team response data."""
    id: int
    
    class Config:
        from_attributes = True  # Allows conversion from SQLAlchemy models


# Player Schemas
class PlayerBase(BaseModel):
    """Base schema for Player with common fields."""
    first_name: str
    last_name: str
    position: str


class PlayerCreate(PlayerBase):
    """Schema for creating a new player."""
    pass


class PlayerResponse(PlayerBase):
    """Schema for player response data."""
    id: int
    
    class Config:
        from_attributes = True


# Season Schemas
class SeasonBase(BaseModel):
    """Base schema for Season with common fields."""
    year: int


class SeasonCreate(SeasonBase):
    """Schema for creating a new season."""
    pass


class SeasonResponse(SeasonBase):
    """Schema for season response data."""
    id: int
    
    class Config:
        from_attributes = True


# RosterMembership Schemas
class RosterMembershipBase(BaseModel):
    """Base schema for RosterMembership with common fields."""
    team_id: int
    player_id: int
    season_id: int


class RosterMembershipCreate(RosterMembershipBase):
    """Schema for creating a new roster membership."""
    pass


class RosterMembershipResponse(RosterMembershipBase):
    """Schema for roster membership response data."""
    id: int
    
    class Config:
        from_attributes = True


# Extended response schemas with relationships
class RosterMembershipDetail(RosterMembershipResponse):
    """Roster membership with full team, player, and season details."""
    team: Optional[TeamResponse] = None
    player: Optional[PlayerResponse] = None
    season: Optional[SeasonResponse] = None

