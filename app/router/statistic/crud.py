from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.core.models import Statistic
from .schemas import StatisticCreateDTO
from app.utils.orm import utils


async def get_statistic(session: AsyncSession, offset: int = 0, limit: int = 0) -> (
        tuple[list[Statistic], int] | list[Statistic]):
    base_query = select(Statistic).order_by(Statistic.id)
    return await utils.get_data(session=session, base_query=base_query, limit=limit, offset=offset)


async def get_statistic_by_device_id(session: AsyncSession, device_id: int, offset: int = 0, limit: int = 0) -> (
        tuple[list[Statistic], int]):
    base_query = select(Statistic).filter_by(device_id=device_id)
    return await utils.get_data(session=session, base_query=base_query, limit=limit, offset=offset)


async def create_statistic(session: AsyncSession, statistic_in: StatisticCreateDTO) -> Statistic | None:
    statistic = Statistic(**statistic_in.model_dump())
    session.add(statistic)
    await session.commit()
    return statistic


