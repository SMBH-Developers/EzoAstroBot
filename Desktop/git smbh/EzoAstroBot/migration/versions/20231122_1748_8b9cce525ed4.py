"""sending

Revision ID: 8b9cce525ed4
Revises: b8325ddc1cc2
Create Date: 2023-11-22 17:48:42.820808

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b9cce525ed4'
down_revision = 'b8325ddc1cc2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('nov22_2_sending', sa.TIMESTAMP(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'nov22_2_sending')
    # ### end Alembic commands ###
