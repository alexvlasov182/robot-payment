"""Add robots table

Revision ID: 86ab8bd5a6b4
Revises: 9b2546c44dfb
Create Date: 2026-07-19 13:30:48.000000+00:00

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "86ab8bd5a6b4"
down_revision: Union[str, None] = "9b2546c44dfb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Створюємо таблицю robots
    op.create_table(
        "robots",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("robot_type", sa.String(), nullable=False),
        sa.Column("status", sa.String(), nullable=True),
        sa.Column("serial_number", sa.String(), nullable=False),
        sa.Column("capabilities", sa.String(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("serial_number"),
    )
    op.create_index("ix_robots_id", "robots", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_robots_id", table_name="robots")
    op.drop_table("robots")
