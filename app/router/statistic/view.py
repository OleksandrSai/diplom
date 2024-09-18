from fastapi import APIRouter, Depends
from .schemas import StatisticResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.async_database import async_database
from fastapi import Query
from . import orm

router = APIRouter(tags=["statistic"])


@router.get("/{device_id}", response_model=StatisticResponse)
async def statistic_by_device_id(device_id: int, session: AsyncSession = Depends(async_database.get_scoped_session),
                                 page_index: int = Query(0, alias="pageIndex",
                                                         description="Page index, starting from 0"),
                                 page_size: int = Query(10, alias="pageSize",
                                                        description="Number of items per page")):
    offset = page_index * page_size
    statistic, total_items = await orm.get_statistic_by_device_id(session=session,
                                                                  device_id=device_id,
                                                                  offset=offset,
                                                                  limit=page_size
                                                                  )

    return {
        "items": statistic,
        "totalItems": total_items
    }


@router.get("/detail-stat/{device_id}")
async def stat(device_id: int,
               session: AsyncSession = Depends(async_database.get_scoped_session),
               date_range: str = Query("", alias="dateRange", description="Page index, starting from 0")):
    return await orm.get_statistic_trend_by_date(session=session, device_id=device_id, date_range=date_range)
