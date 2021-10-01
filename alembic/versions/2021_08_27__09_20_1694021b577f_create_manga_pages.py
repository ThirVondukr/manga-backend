"""Create manga pages

Revision ID: 1694021b577f
Revises: ebe62ac28358
Create Date: 2021-08-27 09:20:01.058351

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "1694021b577f"
down_revision = "ebe62ac28358"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "manga__pages",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("imageUrl", sa.String(), nullable=False),
        sa.Column("chapter_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["chapter_id"],
            ["manga__chapters.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("manga__pages")
