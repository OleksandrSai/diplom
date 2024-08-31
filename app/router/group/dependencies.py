from typing import Annotated
from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.async_database import async_database
from app.core.models import Group
from . import crud


async def group_by_id(
    group_id: Annotated[int, Path],
    session: AsyncSession = Depends(async_database.get_scoped_session),
) -> Group:
    group = await crud.get_group(session=session, group_id=group_id)
    if group is not None:
        return group

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Group {group_id} not found!",
    )
