from fastapi import APIRouter, Depends
from . import crud
from .schemas import SchedulerCreateDTO
from sqlalchemy.ext.asyncio import AsyncSession
from api.core.async_database import async_database
from .schemas import SchedulerDTO

router = APIRouter(tags=["scheduler"])


@router.get("/", response_model=list[SchedulerDTO])
async def get_schedulers(session: AsyncSession = Depends(async_database.get_scoped_session)):
    return await crud.get_schedulers(session=session)


@router.get("/", response_model=SchedulerDTO)
async def create_scheduler(scheduler_id: int, session: AsyncSession = Depends(async_database.get_scoped_session)):
    scheduler = await crud.get_scheduler(session=session, scheduler_id=scheduler_id)
    if scheduler:
        return scheduler


@router.post("/", response_model=SchedulerDTO)
async def create_scheduler(scheduler_in: SchedulerCreateDTO,
                           session: AsyncSession = Depends(async_database.get_scoped_session)):
    return await crud.create_scheduler(session=session, scheduler_in=scheduler_in)
