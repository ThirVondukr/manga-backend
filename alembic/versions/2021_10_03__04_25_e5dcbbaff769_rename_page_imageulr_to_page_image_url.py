"""Rename Page.imageUlr to Page.image_url

Revision ID: e5dcbbaff769
Revises: 8ac1229f6113
Create Date: 2021-10-03 04:25:56.006422

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "e5dcbbaff769"
down_revision = "8ac1229f6113"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(table_name="manga__pages", column_name="imageUrl", new_column_name="image_url")


def downgrade():
    op.alter_column(table_name="manga__pages", column_name="image_url", new_column_name="imageUrl")
