from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result
from api.core.models import Scheduler
from .schemas import SchedulerCreateDTO


async def get_schedulers(session: AsyncSession) -> list[Scheduler]:
    stmt = select(Scheduler).order_by(Scheduler.id)
    result: Result = await session.execute(stmt)
    schedulers = result.scalars().all()
    return list(schedulers)


async def get_scheduler(session: AsyncSession, scheduler_id: int) -> Scheduler | None:
    return await session.get(Scheduler, scheduler_id)


async def create_scheduler(session: AsyncSession, scheduler_in: SchedulerCreateDTO) -> Scheduler | None:
    product = Scheduler(**scheduler_in.model_dump())
    session.add(product)
    await session.commit()
    return product







