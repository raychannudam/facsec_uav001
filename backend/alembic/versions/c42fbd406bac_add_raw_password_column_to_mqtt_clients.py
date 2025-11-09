"""Add raw_password column to mqtt_clients

Revision ID: c42fbd406bac
Revises: d6c8d00f9e06
Create Date: 2025-11-09 04:04:51.932122

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c42fbd406bac'
down_revision: Union[str, Sequence[str], None] = 'd6c8d00f9e06'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add raw_password column to mqtt_clients table
    op.add_column('mqtt_clients', 
        sa.Column('raw_password', sa.String(length=255), nullable=True)
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Remove raw_password column from mqtt_clients table
    op.drop_column('mqtt_clients', 'raw_password')