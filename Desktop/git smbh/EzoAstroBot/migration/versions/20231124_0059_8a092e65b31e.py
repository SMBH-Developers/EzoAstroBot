"""sending

Revision ID: 8a092e65b31e
Revises: 5d677acd29b0
Create Date: 2023-11-24 00:59:08.910495

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8a092e65b31e'
down_revision = '5d677acd29b0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('nov24_sending', sa.TIMESTAMP(), nullable=True))
    op.add_column('users', sa.Column('nov24_2_sending', sa.TIMESTAMP(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'nov24_2_sending')
    op.drop_column('users', 'nov24_sending')
    # ### end Alembic commands ###
