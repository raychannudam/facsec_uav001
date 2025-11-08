"""Merge all heads into one unified branch

Revision ID: d6c8d00f9e06
Revises: 4b212724d225, 6e2a8c7f0573, cf24949fce62
Create Date: 2025-11-08 03:39:28.181924

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd6c8d00f9e06'
down_revision: Union[str, Sequence[str], None] = ('4b212724d225', '6e2a8c7f0573', 'cf24949fce62')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
