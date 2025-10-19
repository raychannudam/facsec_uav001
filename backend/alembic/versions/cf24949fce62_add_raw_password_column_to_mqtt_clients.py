"""add raw_password column to mqtt_clients

Revision ID: cf24949fce62
Revises: e76c4114feed
Create Date: 2025-10-19 05:51:31.917934

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cf24949fce62'
down_revision: Union[str, Sequence[str], None] = 'e76c4114feed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
