from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result
from app.core.models import Scheduler
from .schemas import SchedulerCreateDTO, SchedulerUpdatePartialDTO, SchedulerUpdateDTO


async def get_schedulers(session: AsyncSession) -> list[Scheduler]:
    stmt = select(Scheduler)
    result: Result = await session.execute(stmt)
    schedulers = result.scalars().all()
    return list(schedulers)


async def get_scheduler(session: AsyncSession, scheduler_id: int) -> Scheduler | None:
    return await session.get(Scheduler, scheduler_id)


async def create_scheduler(session: AsyncSession, scheduler_in: SchedulerCreateDTO) -> Scheduler | None:
    scheduler = Scheduler(**scheduler_in.model_dump())
    session.add(scheduler)
    await session.commit()
    return scheduler


async def update_scheduler(session: AsyncSession,
                           scheduler_update: SchedulerUpdatePartialDTO | SchedulerUpdateDTO,
                           scheduler: Scheduler,
                           partial: bool = False) -> Scheduler:
    for key, value in scheduler_update.model_dump(exclude_unset=partial).items():
        setattr(scheduler, key, value)
    await session.commit()
    return scheduler


async def delete_scheduler(session: AsyncSession, scheduler: Scheduler) -> None:
    await session.delete(scheduler)
    await session.commit()
