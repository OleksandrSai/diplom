from typing import Annotated
from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.async_database import async_database
from app.core.models import Scheduler
from . import crud


async def scheduler_by_id(
    scheduler_id: Annotated[int, Path],
    session: AsyncSession = Depends(async_database.get_scoped_session),
) -> Scheduler:
    scheduler = await crud.get_scheduler(session=session, scheduler_id=scheduler_id)
    if scheduler is not None:
        return scheduler

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Scheduler {scheduler_id} not found!",
    )
