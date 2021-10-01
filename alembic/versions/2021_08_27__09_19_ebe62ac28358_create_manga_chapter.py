"""Create manga chapter

Revision ID: ebe62ac28358
Revises: 827f487b3170
Create Date: 2021-08-27 09:19:17.600678

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "ebe62ac28358"
down_revision = "827f487b3170"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "manga__chapters",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("language", sa.String(length=2), nullable=False),
        sa.Column("number", sa.String(length=255), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("manga__chapters")
