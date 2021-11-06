"""empty message

Revision ID: 4cddcd937e3f
Revises: 6fc7326f6818
Create Date: 2021-11-02 21:45:51.444190

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "4cddcd937e3f"
down_revision = "6fc7326f6818"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "manga__chapters",
        "number",
        type_=sa.Integer(),
        nullable=False,
        postgresql_using="number::integer",
    )
    op.add_column("manga__chapters", sa.Column("number_extra", sa.Integer(), nullable=True))


def downgrade():
    op.alter_column(
        "manga__chapters",
        "number",
        type_=sa.String(length=255),
        nullable=False,
    )
    op.drop_column("manga__chapters", "number_extra")
