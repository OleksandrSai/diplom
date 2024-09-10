from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.core.models import Statistic
from .schemas import StatisticCreateDTO


async def get_statistic(session: AsyncSession, offset: int = 0, limit: int = 0) -> (
        tuple[list[Statistic], int] | list[Statistic]):
    base_query = select(Statistic).order_by(Statistic.id)

    total_items = None

    if limit:
        subquery = base_query.subquery()
        count_query = select(func.count()).select_from(subquery)
        paginated_query = base_query.offset(offset).limit(limit)
        total_items_result = await session.execute(count_query)
        total_items = total_items_result.scalar()
        result = await session.execute(paginated_query)
    else:
        result = await session.execute(base_query)

    statistic = result.scalars().all()
    if limit:
        return list(statistic), total_items
    else:
        return list(statistic)


async def get_statistic_by_device_id(session: AsyncSession, device_id: int, offset: int = 0, limit: int = 0) -> (
        tuple[list[Statistic], int]):
    base_query = select(Statistic).filter_by(device_id=device_id)

    subquery = base_query.subquery()
    count_query = select(func.count()).select_from(subquery)
    paginated_query = base_query.offset(offset).limit(limit)
    total_items_result = await session.execute(count_query)
    total_items = total_items_result.scalar()
    result = await session.execute(paginated_query)

    statistic = result.scalars().all()

    return list(statistic), total_items


async def create_statistic(session: AsyncSession, statistic_in: StatisticCreateDTO) -> Statistic | None:
    statistic = Statistic(**statistic_in.model_dump())
    session.add(statistic)
    await session.commit()
    return statistic
