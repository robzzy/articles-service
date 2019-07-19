"""Add reviews

Revision ID: 1af0b55e16f7
Revises: fa89c3514433
Create Date: 2019-07-20 01:57:15.219662

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1af0b55e16f7'
down_revision = 'fa89c3514433'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "reviews",
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_at", sa.DateTime, nullable=False),

        sa.Column("id", sa.Integer, nullable=False),
        sa.Column("content", sa.String(256), nullable=True),
        sa.Column("author_id", sa.Integer, nullable=False),
        sa.Column("article_id", sa.Integer, nullable=False),

        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ("author_id",), ["authors.id"], name="fk_reviews_authors",
        ),
        sa.ForeignKeyConstraint(
            ("article_id",), ["articles.id"], name="fk_reviews_articles",
        )
    )


def downgrade():
    op.drop_table("reviews")
