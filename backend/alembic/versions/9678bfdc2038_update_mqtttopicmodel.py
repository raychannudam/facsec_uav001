"""Update MqttTopicModel

Revision ID: 9678bfdc2038
Revises: c42fbd406bac
Create Date: 2025-11-16 08:00:00

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision: str = '9678bfdc2038'
down_revision: Union[str, Sequence[str], None] = 'c42fbd406bac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema safely."""
    conn = op.get_bind()
    inspector = inspect(conn)
    columns = [col['name'] for col in inspector.get_columns('mqtt_topics')]

    if 'is_default' not in columns:
        # Step 1: Add column with default value to avoid nulls
        op.add_column(
            'mqtt_topics',
            sa.Column('is_default', sa.Boolean(), nullable=False, server_default=sa.false())
        )
        # Step 2: Remove server_default if you don't want it for future rows
        op.alter_column('mqtt_topics', 'is_default', server_default=None)
    else:
        # Column exists, make sure all existing rows are non-null
        op.execute("UPDATE mqtt_topics SET is_default = false WHERE is_default IS NULL")
        op.alter_column('mqtt_topics', 'is_default', nullable=False)


def downgrade() -> None:
    """Downgrade schema safely."""
    conn = op.get_bind()
    inspector = inspect(conn)
    columns = [col['name'] for col in inspector.get_columns('mqtt_topics')]

    if 'is_default' in columns:
        # Allow nulls again
        op.alter_column('mqtt_topics', 'is_default', nullable=True)
