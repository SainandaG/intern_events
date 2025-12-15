"""update event model

Revision ID: c5ce3c74bc8e
Revises: 8664bdfe85d8
Create Date: 2025-12-12 14:46:30.733592
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

revision: str = 'c5ce3c74bc8e'
down_revision: Union[str, None] = '8664bdfe85d8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('events', sa.Column('organization_id', sa.Integer(), nullable=False))
    op.add_column('events', sa.Column('name', sa.String(length=255), nullable=False))
    op.add_column('events', sa.Column('category_id', sa.Integer(), nullable=False))
    op.add_column('events', sa.Column('event_type_id', sa.Integer(), nullable=False))
    op.add_column('events', sa.Column('event_date', sa.DateTime(), nullable=False))
    op.add_column('events', sa.Column('start_time', sa.DateTime(), nullable=True))
    op.add_column('events', sa.Column('end_time', sa.DateTime(), nullable=True))
    op.add_column('events', sa.Column('state', sa.String(length=100), nullable=True))
    op.add_column('events', sa.Column('expected_attendees', sa.Integer(), nullable=True))
    op.add_column('events', sa.Column('actual_attendees', sa.Integer(), nullable=True))
    op.add_column('events', sa.Column('budget', sa.Numeric(15, 2), nullable=True))
    op.add_column('events', sa.Column('special_requirements', sa.Text(), nullable=True))
    op.add_column('events', sa.Column('status', sa.Enum(
        'PLANNING', 'CONFIRMED', 'ACTIVE', 'COMPLETED', 'CANCELLED',
        name='event_status_enum'
    ), nullable=True))
    op.add_column('events', sa.Column('event_manager_id', sa.Integer(), nullable=True))

    # Named Foreign Keys
    op.create_foreign_key('fk_events_category', 'events', 'categories', ['category_id'], ['id'])
    op.create_foreign_key('fk_events_org', 'events', 'organizations', ['organization_id'], ['id'])
    op.create_foreign_key('fk_events_manager', 'events', 'users', ['event_manager_id'], ['id'])
    op.create_foreign_key('fk_events_event_type', 'events', 'event_types', ['event_type_id'], ['id'])

    # Drop old columns
    op.drop_column('events', 'end_date')
    op.drop_column('events', 'title')
    op.drop_column('events', 'start_date')


def downgrade() -> None:
    # Add old columns back
    op.add_column('events', sa.Column('start_date', mysql.DATETIME(), nullable=True))
    op.add_column('events', sa.Column('title', mysql.VARCHAR(length=255), nullable=False))
    op.add_column('events', sa.Column('end_date', mysql.DATETIME(), nullable=True))

    # Drop named FKs
    op.drop_constraint('fk_events_event_type', 'events', type_='foreignkey')
    op.drop_constraint('fk_events_manager', 'events', type_='foreignkey')
    op.drop_constraint('fk_events_org', 'events', type_='foreignkey')
    op.drop_constraint('fk_events_category', 'events', type_='foreignkey')

    # Drop new columns
    op.drop_column('events', 'event_manager_id')
    op.drop_column('events', 'status')
    op.drop_column('events', 'special_requirements')
    op.drop_column('events', 'budget')
    op.drop_column('events', 'actual_attendees')
    op.drop_column('events', 'expected_attendees')
    op.drop_column('events', 'state')
    op.drop_column('events', 'end_time')
    op.drop_column('events', 'start_time')
    op.drop_column('events', 'event_date')
    op.drop_column('events', 'event_type_id')
    op.drop_column('events', 'category_id')
    op.drop_column('events', 'name')
    op.drop_column('events', 'organization_id')
