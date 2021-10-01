"""Add published_at field do Chapter

Revision ID: a3bab1ce971e
Revises: 262e0339da80
Create Date: 2021-08-29 21:26:44.088910

"""
from datetime import datetime

import sqlalchemy as sa
from alembic import op
from sqlalchemy import MetaData, Table
from sqlalchemy.orm import sessionmaker

# revision identifiers, used by Alembic.
revision = "a3bab1ce971e"
down_revision = "262e0339da80"
branch_labels = None
depends_on = None

Session = sessionmaker()


def upgrade():
    op.add_column(
        "manga__chapters",
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
    )

    meta = MetaData(op.get_bind())
    meta.reflect()

    now = datetime.utcnow()
    chapters_table = Table("manga__chapters", meta)
    op.execute(chapters_table.update().values(published_at=now))

    op.alter_column("manga__chapters", "published_at", nullable=False)


def downgrade():
    op.drop_column("manga__chapters", "published_at")
