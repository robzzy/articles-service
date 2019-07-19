"""Add authors and articles

Revision ID: fa89c3514433
Revises: 
Create Date: 2019-07-20 01:39:55.226755

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa89c3514433'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():

    op.create_table(
        "authors",
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_at", sa.DateTime, nullable=False),
        sa.Column("id", sa.Integer, nullable=False),
        sa.Column("nickname", sa.String(64), nullable=False),
        sa.Column("gender", sa.String(8), nullable=True),
        sa.Column("birth", sa.DateTime, nullable=True),
        sa.Column("location", sa.String(64), nullable=True),
        sa.Column("user_uuid", sa.String(36), nullable=False, unique=True),

        sa.PrimaryKeyConstraint("id"),
        mysql_charset="utf8mb4",
        mysql_collate="utf8mb4_general_ci",
        mysql_engine="InnoDB",
    )

    op.create_table(
        "articles",
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_at", sa.DateTime, nullable=False),

        sa.Column("id", sa.Integer, nullable=False),
        sa.Column("title", sa.String(32), nullable=False),
        sa.Column("content", sa.Text, nullable=True),
        sa.Column("status", sa.String(16), nullable=False),
        sa.Column("click_num", sa.Integer, nullable=True),
        sa.Column("author_id", sa.Integer, nullable=False),

        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ("author_id",), ["authors.id"], name="fk_articles_authors",
        ),
    )


def downgrade():
    op.drop_table("articles")
    op.drop_table("authors")
