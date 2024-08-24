"""update colum, add statistic

Revision ID: 9fb2e92ba1e7
Revises: 8e15af4213e9
Create Date: 2024-08-11 21:08:15.276997

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9fb2e92ba1e7'
down_revision: Union[str, None] = '8e15af4213e9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('group',
    sa.Column('name', sa.String(length=256), nullable=False),
    sa.Column('strategy', sa.Enum('TimeWorks', 'MaximumPowerConsumption', 'PeakEnergyConsumption', 'EnergyEfficiency', 'PercentageOfNetworkLoad', 'DurationOfOperatingTimeAtHighPower', 'AverageEnergyConsumptionPerHour', name='strategy'), nullable=False),
    sa.Column('value_strategy', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('groupdevicepriority',
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.Column('device_id', sa.Integer(), nullable=False),
    sa.Column('priority', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['device_id'], ['device.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['group_id'], ['group.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('statistic',
    sa.Column('device_id', sa.Integer(), nullable=False),
    sa.Column('instant_current', sa.Float(), nullable=False),
    sa.Column('instant_voltage', sa.Float(), nullable=False),
    sa.Column('total_consumption', sa.Float(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['device_id'], ['device.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('device', sa.Column('name', sa.String(length=256), nullable=False))
    op.add_column('device', sa.Column('nwk_adr', sa.String(length=256), nullable=False))
    op.add_column('device', sa.Column('status', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('device', 'status')
    op.drop_column('device', 'nwk_adr')
    op.drop_column('device', 'name')
    op.drop_table('statistic')
    op.drop_table('groupdevicepriority')
    op.drop_table('group')
    # ### end Alembic commands ###
