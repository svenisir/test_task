"""Edit table memes, delete column mem_picture

Revision ID: 687ce5f99628
Revises: f1af382044f4
Create Date: 2024-06-21 00:59:22.811189

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '687ce5f99628'
down_revision: Union[str, None] = 'f1af382044f4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('memes', 'mem_picture')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('memes', sa.Column('mem_picture', sa.VARCHAR(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
