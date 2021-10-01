"""Make datetime fields non-nullable

Revision ID: 827f487b3170
Revises: deec5fb628c9
Create Date: 2021-08-27 09:13:49.994574

"""
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "827f487b3170"
down_revision = "deec5fb628c9"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "manga__manga",
        "created_at",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=False,
    )
    op.alter_column(
        "manga__manga",
        "updated_at",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=False,
    )


def downgrade():
    op.alter_column(
        "manga__manga",
        "updated_at",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=True,
    )
    op.alter_column(
        "manga__manga",
        "created_at",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=True,
    )
