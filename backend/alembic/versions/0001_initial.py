"""initial schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-10-31 00:00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "admin_user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=50), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_admin_user_username"),
        "admin_user",
        ["username"],
        unique=True,
    )

    op.create_table(
        "profile",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("avatar_url", sa.String(length=500), nullable=False),
        sa.Column("bio", sa.String(length=500), nullable=False),
        sa.Column("typing_slogan", sa.String(length=200), nullable=False),
        sa.Column("wechat", sa.String(length=100), nullable=True),
        sa.Column("email", sa.String(length=100), nullable=True),
        sa.Column("github_url", sa.String(length=500), nullable=True),
        sa.Column("radar_skills", sa.Text(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "project",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("summary", sa.String(length=500), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("cover_image", sa.String(length=500), nullable=True),
        sa.Column("project_images", sa.Text(), nullable=True),
        sa.Column("tech_stack", sa.String(length=500), nullable=False),
        sa.Column("demo_url", sa.String(length=500), nullable=True),
        sa.Column("github_url", sa.String(length=500), nullable=True),
        sa.Column("category", sa.String(length=50), nullable=False),
        sa.Column("is_published", sa.Boolean(), nullable=False),
        sa.Column("views_count", sa.Integer(), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("project")
    op.drop_table("profile")
    op.drop_index(op.f("ix_admin_user_username"), table_name="admin_user")
    op.drop_table("admin_user")
