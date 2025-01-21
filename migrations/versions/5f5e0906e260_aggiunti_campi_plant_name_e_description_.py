"""Aggiunti campi plant_name e description a LeafImage

Revision ID: 5f5e0906e260
Revises: 3c456b7aec8b
Create Date: 2025-01-21 11:05:02.925171

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f5e0906e260'
down_revision = '3c456b7aec8b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('leaf_image', schema=None) as batch_op:
        batch_op.add_column(sa.Column('plant_name', sa.String(length=150), nullable=True))
        batch_op.add_column(sa.Column('description', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('leaf_image', schema=None) as batch_op:
        batch_op.drop_column('description')
        batch_op.drop_column('plant_name')

    # ### end Alembic commands ###
