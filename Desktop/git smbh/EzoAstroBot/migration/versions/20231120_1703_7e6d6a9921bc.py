"""sending

Revision ID: 7e6d6a9921bc
Revises: f9914df6f4e3
Create Date: 2023-11-20 17:03:24.710038

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e6d6a9921bc'
down_revision = 'f9914df6f4e3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('nov20_sending', sa.TIMESTAMP(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'nov20_sending')
    # ### end Alembic commands ###
