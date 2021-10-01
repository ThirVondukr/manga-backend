"""Rename Users Table

Revision ID: a2f3c00ada16
Revises: c2587dc7c10f
Create Date: 2021-08-22 11:32:48.864952

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "a2f3c00ada16"
down_revision = "c2587dc7c10f"
branch_labels = None
depends_on = None


def upgrade():
    op.rename_table("users.users", "users__users")


def downgrade():
    op.rename_table("users__users", "users.users")
