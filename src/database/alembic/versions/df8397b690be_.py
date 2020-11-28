"""

Revision ID: df8397b690be
Revises: 
Create Date: 2020-11-28 16:06:26.042997

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'df8397b690be'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "utters",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("template", sa.VARCHAR(), nullable=False),
        sa.Column("channel", sa.VARCHAR(), nullable=False),
        sa.Column("responses", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id")
    )
    op.create_index(op.f("unique_template_by_channel"), "utters", ["template", "channel"], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("unique_template_by_channel"), table_name="utters")
    op.drop_table("utters")
    # ### end Alembic commands ###
