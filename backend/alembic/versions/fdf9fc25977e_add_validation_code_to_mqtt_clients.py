"""Add validation_code to mqtt_clients

Revision ID: fdf9fc25977e
Revises: b3c54b25f2e8
Create Date: 2025-10-19 04:26:00.511555

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision: str = 'fdf9fc25977e'
down_revision: Union[str, Sequence[str], None] = 'b3c54b25f2e8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()
    inspector = inspect(conn)
    # Only add the column if it doesn't already exist
    if 'validation_code' not in [c['name'] for c in inspector.get_columns('mqtt_clients')]:
        op.add_column('mqtt_clients', sa.Column('validation_code', sa.String(length=6), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    conn = op.get_bind()
    inspector = inspect(conn)
    # Only drop the column if it exists
    if 'validation_code' in [c['name'] for c in inspector.get_columns('mqtt_clients')]:
        op.drop_column('mqtt_clients', 'validation_code')
