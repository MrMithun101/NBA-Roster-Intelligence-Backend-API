"""Roster service: db access for team roster by season."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Player, RosterMembership, Season, Team


def get_roster_for_team_season(
    session: Session, team_id: int, season_year: int
) -> tuple[list[Player], Team | None, Season | None]:
    """
    Return (list of players on the roster, team or None, season or None).
    If team or season not found, returns ([], None, None) or ([], team, None) etc.
    """
    team = session.execute(select(Team).where(Team.id == team_id)).scalar_one_or_none()
    if not team:
        return [], None, None

    season = (
        session.execute(select(Season).where(Season.year == season_year))
        .scalar_one_or_none()
    )
    if not season:
        return [], team, None

    stmt = (
        select(Player)
        .join(RosterMembership, RosterMembership.player_id == Player.id)
        .where(
            RosterMembership.team_id == team_id,
            RosterMembership.season_id == season.id,
        )
        .order_by(Player.last_name, Player.first_name)
    )
    result = session.execute(stmt)
    players = list(result.unique().scalars().all())
    return players, team, season
