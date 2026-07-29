"""Add robots table

Revision ID: 86ab8bd5a6b4
Revises: 9b2546c44dfb
Create Date: 2026-07-19 13:30:48.000000+00:00

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "86ab8bd5a6b4"
down_revision: Union[str, None] = "9b2546c44dfb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
