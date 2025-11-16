"""Update ControllerModel

Revision ID: b3c54b25f2e8
Revises: fa8938c32b11
Create Date: 2025-10-16 02:32:07.950547
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'b3c54b25f2e8'
down_revision: Union[str, Sequence[str], None] = 'fa8938c32b11'
branch_labels = None
depends_on = None


def upgrade() -> None:
    conn = op.get_bind()

    # Check if the column exists
    col_exists = conn.execute(
        sa.text("""
            SELECT 1
            FROM information_schema.columns
            WHERE table_name='controllers'
              AND column_name='user_id'
        """)
    ).fetchone()

    if not col_exists:
        op.add_column('controllers', sa.Column('user_id', sa.Integer(), nullable=False))

    # Check if the foreign key exists
    fk_exists = conn.execute(
        sa.text("""
            SELECT 1
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
            ON tc.constraint_name = kcu.constraint_name
            WHERE tc.table_name = 'controllers'
              AND tc.constraint_type = 'FOREIGN KEY'
              AND kcu.column_name = 'user_id'
        """)
    ).fetchone()

    if not fk_exists:
        op.create_foreign_key(None, 'controllers', 'users', ['user_id'], ['id'], ondelete='CASCADE')


def downgrade() -> None:
    conn = op.get_bind()

    # Drop foreign key if it exists
    fk_list = conn.execute(
        sa.text("""
            SELECT constraint_name
            FROM information_schema.table_constraints
            WHERE table_name = 'controllers'
              AND constraint_type = 'FOREIGN KEY'
        """)
    ).fetchall()

    for (fk_name,) in fk_list:
        op.drop_constraint(fk_name, 'controllers', type_='foreignkey')

    # Drop column if it exists
    col_exists = conn.execute(
        sa.text("""
            SELECT 1
            FROM information_schema.columns
            WHERE table_name='controllers'
              AND column_name='user_id'
        """)
    ).fetchone()

    if col_exists:
        op.drop_column('controllers', 'user_id')
