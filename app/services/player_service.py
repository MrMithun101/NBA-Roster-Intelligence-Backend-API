"""Player service: db access for players with optional filters and pagination."""

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.models import Player, RosterMembership


def get_players(
    session: Session,
    *,
    team_id: int | None = None,
    position: str | None = None,
    name: str | None = None,
    limit: int = 20,
    offset: int = 0,
) -> tuple[list[Player], int]:
    """
    Return (list of players, total count) with optional filters and pagination.
    - team_id: only players who were on this team (in any season)
    - position: exact match
    - name: case-insensitive search on first_name + last_name
    """
    base = select(Player)
    count_base = select(func.count()).select_from(Player)

    if team_id is not None:
        subq = select(RosterMembership.player_id).where(
            RosterMembership.team_id == team_id
        ).distinct()
        base = base.where(Player.id.in_(subq))
        count_base = count_base.where(Player.id.in_(subq))

    if position is not None and position.strip() != "":
        base = base.where(Player.position == position.strip())
        count_base = count_base.where(Player.position == position.strip())

    if name is not None and name.strip() != "":
        pattern = f"%{name.strip()}%"
        name_filter = or_(
            Player.first_name.ilike(pattern),
            Player.last_name.ilike(pattern),
        )
        base = base.where(name_filter)
        count_base = count_base.where(name_filter)

    total = session.execute(count_base).scalar_one() or 0
    stmt = base.order_by(Player.last_name, Player.first_name).limit(limit).offset(offset)
    result = session.execute(stmt)
    rows = list(result.scalars().all())
    return rows, total
