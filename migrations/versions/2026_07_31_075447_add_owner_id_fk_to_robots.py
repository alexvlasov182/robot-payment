"""add owner_id fk to robots
Revision ID: a492466e6f9f
Revises: 7553872aefd1
Create Date: 2026-07-31 07:54:47.254788+00:00
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a492466e6f9f'
down_revision: Union[str, None] = '7553872aefd1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Add the column as nullable first
    op.add_column('robots', sa.Column('owner_id', sa.Integer(), nullable=True))

    # 2. Assign existing robots to the first user (id=1) as a data migration.
    #    Safe for this dataset: production currently has exactly one user and one robot.
    op.execute("UPDATE robots SET owner_id = 1 WHERE owner_id IS NULL")

    # 3. Now enforce NOT NULL, index, and FK
    op.alter_column('robots', 'owner_id', nullable=False)
    op.create_index(op.f('ix_robots_owner_id'), 'robots', ['owner_id'], unique=False)
    op.create_foreign_key(None, 'robots', 'users', ['owner_id'], ['id'], ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint(None, 'robots', type_='foreignkey')
    op.drop_index(op.f('ix_robots_owner_id'), table_name='robots')
    op.drop_column('robots', 'owner_id')
