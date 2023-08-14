"""Init.

Revision ID: bc6cace70c50
Revises:
Create Date: 2023-08-15 03:37:40.918504

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "bc6cace70c50"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "ingredients",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("image", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "recipes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("image", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "recipes_ingredients",
        sa.Column("recipe_id", sa.Integer(), nullable=False),
        sa.Column("ingredient_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["ingredient_id"],
            ["ingredients.id"],
        ),
        sa.ForeignKeyConstraint(
            ["recipe_id"],
            ["recipes.id"],
        ),
        sa.PrimaryKeyConstraint("recipe_id", "ingredient_id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("recipes_ingredients")
    op.drop_table("recipes")
    op.drop_table("ingredients")
    # ### end Alembic commands ###
