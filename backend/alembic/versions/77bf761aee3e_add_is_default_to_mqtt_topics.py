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
    """Upgrade schema safely."""
    conn = op.get_bind()
    inspector = inspect(conn)

    columns = [col['name'] for col in inspector.get_columns('mqtt_topics')]
    if 'is_default' not in columns:
        # Add column with a default value to avoid nulls
        op.add_column(
            'mqtt_topics',
            sa.Column('is_default', sa.Boolean(), nullable=False, server_default=sa.false())
        )
        # Remove server_default if you don't want it for new rows
        op.alter_column('mqtt_topics', 'is_default', server_default=None)
    else:
        # Ensure existing column is NOT NULL
        op.execute("UPDATE mqtt_topics SET is_default = false WHERE is_default IS NULL")
        op.alter_column('mqtt_topics', 'is_default', nullable=False)


def downgrade() -> None:
    """Downgrade schema safely."""
    conn = op.get_bind()
    inspector = inspect(conn)

    columns = [col['name'] for col in inspector.get_columns('mqtt_topics')]
    if 'is_default' in columns:
        op.alter_column('mqtt_topics', 'is_default', nullable=True)