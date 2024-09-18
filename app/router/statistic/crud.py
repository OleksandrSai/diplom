from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.models import Statistic
from .schemas import StatisticCreateDTO
from app.utils.dependencies import get_data


async def get_statistic(session: AsyncSession, offset: int = 0, limit: int = 0) -> (
        tuple[list[Statistic], int] | list[Statistic]):
    base_query = select(Statistic).order_by(Statistic.id)
    return await get_data(session=session, base_query=base_query, limit=limit, offset=offset)


async def create_statistic(session: AsyncSession, statistic_in: StatisticCreateDTO) -> Statistic | None:
    statistic = Statistic(**statistic_in.model_dump())
    session.add(statistic)
    await session.commit()
    return statistic


