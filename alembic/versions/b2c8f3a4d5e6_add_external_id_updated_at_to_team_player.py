"""add external_id and updated_at to team and player

Revision ID: b2c8f3a4d5e6
Revises: e91df916ab7b
Create Date: 2025-02-01

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'b2c8f3a4d5e6'
down_revision: Union[str, None] = 'e91df916ab7b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('teams', sa.Column('external_id', sa.String(length=32), nullable=True))
    op.add_column('teams', sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    op.create_index(op.f('ix_teams_external_id'), 'teams', ['external_id'], unique=True)

    op.add_column('players', sa.Column('external_id', sa.String(length=32), nullable=True))
    op.add_column('players', sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    op.create_index(op.f('ix_players_external_id'), 'players', ['external_id'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_players_external_id'), table_name='players')
    op.drop_column('players', 'updated_at')
    op.drop_column('players', 'external_id')

    op.drop_index(op.f('ix_teams_external_id'), table_name='teams')
    op.drop_column('teams', 'updated_at')
    op.drop_column('teams', 'external_id')
