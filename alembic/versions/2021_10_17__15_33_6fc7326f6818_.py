"""empty message

Revision ID: 6fc7326f6818
Revises: e5dcbbaff769
Create Date: 2021-10-17 15:33:28.604815

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "6fc7326f6818"
down_revision = "e5dcbbaff769"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("manga__pages", sa.Column("number", sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("manga__pages", "number")
    # ### end Alembic commands ###
