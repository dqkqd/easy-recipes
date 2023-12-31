""" Rename image column to image_url

Revision ID: 5b88c50f7056
Revises: c40048b46ab4
Create Date: 2023-08-19 19:51:19.329128

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "5b88c50f7056"
down_revision = "c40048b46ab4"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("ingredients", schema=None) as batch_op:
        batch_op.alter_column(column_name="image", new_column_name="image_url")

    with op.batch_alter_table("recipes", schema=None) as batch_op:
        batch_op.alter_column(column_name="image", new_column_name="image_url")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("recipes", schema=None) as batch_op:
        batch_op.alter_column(column_name="image_url", new_column_name="image")

    with op.batch_alter_table("ingredients", schema=None) as batch_op:
        batch_op.alter_column(column_name="image_url", new_column_name="image")

    # ### end Alembic commands ###
