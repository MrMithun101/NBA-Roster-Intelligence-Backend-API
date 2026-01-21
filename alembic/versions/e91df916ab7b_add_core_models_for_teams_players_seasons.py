"""add core models for teams players seasons and roster membership

Revision ID: e91df916ab7b
Revises: 
Create Date: 2024-12-19 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e91df916ab7b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create teams table
    op.create_table(
        'teams',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('abbreviation', sa.String(length=3), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_teams_id'), 'teams', ['id'], unique=False)
    op.create_index(op.f('ix_teams_name'), 'teams', ['name'], unique=False)
    op.create_index(op.f('ix_teams_abbreviation'), 'teams', ['abbreviation'], unique=True)
    
    # Create players table
    op.create_table(
        'players',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('first_name', sa.String(), nullable=False),
        sa.Column('last_name', sa.String(), nullable=False),
        sa.Column('position', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_players_id'), 'players', ['id'], unique=False)
    op.create_index(op.f('ix_players_first_name'), 'players', ['first_name'], unique=False)
    op.create_index(op.f('ix_players_last_name'), 'players', ['last_name'], unique=False)
    op.create_index(op.f('ix_players_position'), 'players', ['position'], unique=False)
    
    # Create seasons table
    op.create_table(
        'seasons',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_seasons_id'), 'seasons', ['id'], unique=False)
    op.create_index(op.f('ix_seasons_year'), 'seasons', ['year'], unique=True)
    
    # Create roster_memberships table
    op.create_table(
        'roster_memberships',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('team_id', sa.Integer(), nullable=False),
        sa.Column('player_id', sa.Integer(), nullable=False),
        sa.Column('season_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['player_id'], ['players.id'], ),
        sa.ForeignKeyConstraint(['season_id'], ['seasons.id'], ),
        sa.ForeignKeyConstraint(['team_id'], ['teams.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('team_id', 'player_id', 'season_id', name='unique_roster_membership')
    )
    op.create_index(op.f('ix_roster_memberships_id'), 'roster_memberships', ['id'], unique=False)
    op.create_index(op.f('ix_roster_memberships_team_id'), 'roster_memberships', ['team_id'], unique=False)
    op.create_index(op.f('ix_roster_memberships_player_id'), 'roster_memberships', ['player_id'], unique=False)
    op.create_index(op.f('ix_roster_memberships_season_id'), 'roster_memberships', ['season_id'], unique=False)
    op.create_index('idx_team_season', 'roster_memberships', ['team_id', 'season_id'], unique=False)


def downgrade() -> None:
    # Drop tables in reverse order (respecting foreign key dependencies)
    op.drop_index('idx_team_season', table_name='roster_memberships')
    op.drop_index(op.f('ix_roster_memberships_season_id'), table_name='roster_memberships')
    op.drop_index(op.f('ix_roster_memberships_player_id'), table_name='roster_memberships')
    op.drop_index(op.f('ix_roster_memberships_team_id'), table_name='roster_memberships')
    op.drop_index(op.f('ix_roster_memberships_id'), table_name='roster_memberships')
    op.drop_table('roster_memberships')
    
    op.drop_index(op.f('ix_seasons_year'), table_name='seasons')
    op.drop_index(op.f('ix_seasons_id'), table_name='seasons')
    op.drop_table('seasons')
    
    op.drop_index(op.f('ix_players_position'), table_name='players')
    op.drop_index(op.f('ix_players_last_name'), table_name='players')
    op.drop_index(op.f('ix_players_first_name'), table_name='players')
    op.drop_index(op.f('ix_players_id'), table_name='players')
    op.drop_table('players')
    
    op.drop_index(op.f('ix_teams_abbreviation'), table_name='teams')
    op.drop_index(op.f('ix_teams_name'), table_name='teams')
    op.drop_index(op.f('ix_teams_id'), table_name='teams')
    op.drop_table('teams')

