"""initial tables

Revision ID: 0001
Revises: 
Create Date: 2025-12-29
"""

from alembic import op
import sqlalchemy as sa


revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "crypto_assets",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("symbol", sa.String(20), nullable=False, unique=True),
        sa.Column("name", sa.String(100), nullable=False),
    )

    op.create_table(
        "crypto_prices",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("asset_id", sa.Integer, sa.ForeignKey("crypto_assets.id")),
        sa.Column("source", sa.String(50), nullable=False),
        sa.Column("price_usd", sa.Float, nullable=False),
        sa.Column("fetched_at", sa.DateTime),
        sa.UniqueConstraint("asset_id", "source", name="uq_asset_source"),
    )

    op.create_table(
        "raw_data",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("source", sa.String(50), nullable=False),
        sa.Column("payload", sa.Text, nullable=False),
        sa.Column("ingested_at", sa.DateTime),
    )

    op.create_table(
        "etl_checkpoints",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("source", sa.String(50), nullable=False, unique=True),
        sa.Column("last_run", sa.DateTime),
    )


def downgrade():
    op.drop_table("etl_checkpoints")
    op.drop_table("raw_data")
    op.drop_table("crypto_prices")
    op.drop_table("crypto_assets")
