from fastapi import APIRouter, Depends
from . import crud
from .schemas import StatisticBaseDTO
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.async_database import async_database
from .schemas import SchedulerDTO

router = APIRouter(tags=["statistic"])


@router.get("/{device_id}/", response_model=StatisticBaseDTO)
async def statistic_by_device_id(device_id: int, session: AsyncSession = Depends(async_database.get_scoped_session)):
    statistic = await crud.get_statistic_by_device_id(session=session, device_id=device_id)
    if statistic:
        return statistic

