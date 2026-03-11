"""Team service: db access for teams."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Team


def get_all_teams(session: Session) -> list[Team]:
    stmt = select(Team).order_by(Team.name)
    result = session.execute(stmt)
    return list(result.scalars().all())


def get_team_by_id(session: Session, team_id: int) -> Team | None:
    stmt = select(Team).where(Team.id == team_id)
    return session.execute(stmt).scalar_one_or_none()
