"""Add image_url to MangaArt

Revision ID: 262e0339da80
Revises: 8fcf58bec493
Create Date: 2021-08-28 13:15:24.525113

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "262e0339da80"
down_revision = "8fcf58bec493"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "manga__manga_art",
        sa.Column("image_url", sa.String(length=255), nullable=False),
    )


def downgrade():
    op.drop_column("manga__manga_art", "image_url")
