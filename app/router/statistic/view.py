from fastapi import APIRouter, Depends
from . import crud
from .schemas import StatisticResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.async_database import async_database
from fastapi import Query

router = APIRouter(tags=["statistic"])


@router.get("/{device_id}/", response_model=StatisticResponse)
async def statistic_by_device_id(device_id: int, session: AsyncSession = Depends(async_database.get_scoped_session),
                                 page_index: int = Query(0, alias="pageIndex",
                                                         description="Page index, starting from 0"),
                                 page_size: int = Query(10, alias="pageSize",
                                                        description="Number of items per page")):
    offset = page_index * page_size
    statistic, total_items = await crud.get_statistic_by_device_id(session=session,
                                                                   device_id=device_id,
                                                                   offset=offset,
                                                                   limit=page_size
                                                                   )

    return {
        "items": statistic,
        "totalItems": total_items
    }
