"""Add manga_id col to manga chapter

Revision ID: 8fcf58bec493
Revises: 8eec50ffdd33
Create Date: 2021-08-27 21:46:40.683117

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "8fcf58bec493"
down_revision = "8eec50ffdd33"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "manga__chapters",
        sa.Column("manga_id", postgresql.UUID(as_uuid=True), nullable=False),
    )
    op.create_foreign_key(None, "manga__chapters", "manga__manga", ["manga_id"], ["id"])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "manga__chapters", type_="foreignkey")
    op.drop_column("manga__chapters", "manga_id")
    # ### end Alembic commands ###
