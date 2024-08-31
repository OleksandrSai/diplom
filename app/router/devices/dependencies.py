from typing import Annotated
from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.async_database import async_database
from app.core.models import Device
from . import crud


async def device_by_id(
    device_id: Annotated[int, Path],
    session: AsyncSession = Depends(async_database.get_scoped_session),
) -> Device:
    device = await crud.get_device(session=session, device_id=device_id)
    if device is not None:
        return device

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Device {device_id} not found!",
    )
