"""Add is_default to mqtt_topics

Revision ID: 77bf761aee3e
Revises: 4c380d5ec802
Create Date: 2025-11-16 03:29:30.124737
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision: str = '77bf761aee3e'
down_revision: Union[str, Sequence[str], None] = '4c380d5ec802'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()
    inspector = inspect(conn)
    if 'is_default' not in [c['name'] for c in inspector.get_columns('mqtt_topics')]:
        op.add_column('mqtt_topics', sa.Column('is_default', sa.Boolean(), nullable=True, server_default="false"))


def downgrade() -> None:
    """Downgrade schema."""
    conn = op.get_bind()
    inspector = inspect(conn)
    if 'is_default' in [c['name'] for c in inspector.get_columns('mqtt_topics')]:
        op.drop_column('mqtt_topics', 'is_default')