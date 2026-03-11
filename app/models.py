"""
Database models for NBA roster intelligence.

These models represent the core entities: Teams, Players, Seasons, and
the relationships between them through RosterMembership.
"""

from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db import Base


class Team(Base):
    """
    Represents an NBA team.
    
    Example: Los Angeles Lakers, Boston Celtics, etc.
    external_id: stable ID from external source (e.g. NBA API) for upsert matching.
    updated_at: last time we synced this row from the external source.
    """
    __tablename__ = "teams"
    
    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String(32), unique=True, index=True, nullable=True)  # e.g. NBA API team id
    name = Column(String, nullable=False, index=True)  # e.g., "Los Angeles Lakers"
    abbreviation = Column(String(3), nullable=False, unique=True, index=True)  # e.g., "LAL"
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationship: one team can have many roster memberships
    roster_memberships = relationship("RosterMembership", back_populates="team")


class Player(Base):
    """
    Represents an NBA player.
    
    Example: LeBron James, Stephen Curry, etc.
    external_id: stable ID from external source (e.g. NBA API) for upsert matching.
    updated_at: last time we synced this row from the external source.
    """
    __tablename__ = "players"
    
    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String(32), unique=True, index=True, nullable=True)  # e.g. NBA API player id
    first_name = Column(String, nullable=False, index=True)
    last_name = Column(String, nullable=False, index=True)
    position = Column(String, nullable=False, index=True)  # e.g., "PG", "SG", "SF", "PF", "C"
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationship: one player can have many roster memberships (across different teams/seasons)
    roster_memberships = relationship("RosterMembership", back_populates="player")


class Season(Base):
    """
    Represents an NBA season.
    
    Example: 2023-24 season, 2024-25 season, etc.
    We store just the year (e.g., 2024) to represent the season.
    """
    __tablename__ = "seasons"
    
    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False, unique=True, index=True)  # e.g., 2024
    
    # Relationship: one season can have many roster memberships
    roster_memberships = relationship("RosterMembership", back_populates="season")


class RosterMembership(Base):
    """
    Represents a player being on a team's roster for a specific season.
    
    Why this model exists:
    - A player can be on different teams in different seasons (trades, free agency)
    - A team has different players each season
    - This creates a "many-to-many" relationship: players ↔ teams, across seasons
    
    Example: LeBron James was on the Lakers in 2023-24 season, 
             but was on the Cavaliers in 2017-18 season.
    
    The unique constraint ensures a player can only be on a team once per season
    (prevents duplicate entries).
    """
    __tablename__ = "roster_memberships"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys: links to Team, Player, and Season
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False, index=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False, index=True)
    season_id = Column(Integer, ForeignKey("seasons.id"), nullable=False, index=True)
    
    # Relationships: connect back to the related models
    team = relationship("Team", back_populates="roster_memberships")
    player = relationship("Player", back_populates="roster_memberships")
    season = relationship("Season", back_populates="roster_memberships")
    
    # Unique constraint: a player can only be on a team once per season
    # This prevents duplicate roster entries
    __table_args__ = (
        UniqueConstraint("team_id", "player_id", "season_id", name="unique_roster_membership"),
        # Index for faster queries like "get all players on a team in a season"
        Index("idx_team_season", "team_id", "season_id"),
    )

