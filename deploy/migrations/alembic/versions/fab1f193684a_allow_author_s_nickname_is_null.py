"""Allow author's nickname is NULL

Revision ID: fab1f193684a
Revises: 1af0b55e16f7
Create Date: 2019-07-28 15:07:06.653486

"""
from alembic import op
from sqlalchemy.dialects import mysql


# revision identifiers, used by Alembic.
revision = 'fab1f193684a'
down_revision = '1af0b55e16f7'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "authors",
        "nickname",
        existing_type=mysql.VARCHAR(length=64),
        nullable=True,
    )


def downgrade():
    op.alter_column(
        "authors",
        "nickname",
        existing_type=mysql.VARCHAR(length=64),
        nullable=False,
    )
