from fastapi import APIRouter, Depends, status
from . import crud
from .schemas import SchedulerCreateDTO, SchedulerUpdateDTO, SchedulerUpdatePartialDTO
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.async_database import async_database
from .schemas import SchedulerDTO
from .dependencies import scheduler_by_id
from app.core.models import Scheduler

router = APIRouter(tags=["scheduler"])


@router.get("/", response_model=list[SchedulerDTO])
async def get_schedulers(session: AsyncSession = Depends(async_database.get_scoped_session)):
    return await crud.get_schedulers(session=session)


@router.get("/{scheduler_id}/", response_model=SchedulerDTO)
async def create_scheduler(scheduler_id: int, session: AsyncSession = Depends(async_database.get_scoped_session)):
    scheduler = await crud.get_scheduler(session=session, scheduler_id=scheduler_id)
    if scheduler:
        return scheduler


@router.post("/", response_model=SchedulerDTO)
async def create_scheduler(scheduler_in: SchedulerCreateDTO,
                           session: AsyncSession = Depends(async_database.get_scoped_session)):
    return await crud.create_scheduler(session=session, scheduler_in=scheduler_in)


@router.put("/{scheduler_id}/")
async def update_scheduler(
    scheduler_update: SchedulerUpdateDTO,
    scheduler: Scheduler = Depends(scheduler_by_id),
    session: AsyncSession = Depends(async_database.get_scoped_session),
):
    return await crud.update_scheduler(
        session=session,
        scheduler=scheduler,
        scheduler_update=scheduler_update,
    )


@router.patch("/{scheduler_id}/")
async def update_scheduler_partial(
    scheduler_update: SchedulerUpdatePartialDTO,
    scheduler: Scheduler = Depends(scheduler_by_id),
    session: AsyncSession = Depends(async_database.get_scoped_session),
):
    return await crud.update_scheduler(
        session=session,
        scheduler=scheduler,
        scheduler_update=scheduler_update,
        partial=True,
    )


@router.delete("/{scheduler_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_scheduler(
    scheduler: Scheduler = Depends(scheduler_by_id),
    session: AsyncSession = Depends(async_database.get_scoped_session),
) -> None:
    await crud.delete_scheduler(session=session, scheduler=scheduler)

