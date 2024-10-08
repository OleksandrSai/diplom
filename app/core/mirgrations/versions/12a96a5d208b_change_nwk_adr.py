"""change nwk_adr

Revision ID: 12a96a5d208b
Revises: 36ef0e2124a9
Create Date: 2024-08-31 20:06:58.283746

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '12a96a5d208b'
down_revision: Union[str, None] = '36ef0e2124a9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('device', 'nwk_adr',
               existing_type=mysql.VARCHAR(length=256),
               type_=sa.Integer(),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('device', 'nwk_adr',
               existing_type=sa.Integer(),
               type_=mysql.VARCHAR(length=256),
               existing_nullable=False)
    # ### end Alembic commands ###
