from fastapi import APIRouter, Depends, status, Query
from . import crud
from .schemas import DevicesCreateDTO, DevicesUpdateDTO, DevicesUpdatePartialDTO, DevicesResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.async_database import async_database
from .schemas import DevicesDTO
from .dependencies import device_by_id
from app.core.models import Device

router = APIRouter(tags=["device"])


@router.get("/", response_model=DevicesResponse)
async def get_devices(session: AsyncSession = Depends(async_database.get_scoped_session),
                      page_index: int = Query(0, alias="pageIndex", description="Page index, starting from 0"),
                      page_size: int = Query(10, alias="pageSize", description="Number of items per page"),
                      search_text: str = Query("", alias="searchText", description="Search text")):
    offset = page_index * page_size
    devices, total_items = await crud.get_devices(session=session, offset=offset, limit=page_size, search=search_text)

    return {
        "items": devices,
        "totalItems": total_items
    }


@router.get("/{device_id}/", response_model=DevicesDTO)
async def get_device(device_id: int, session: AsyncSession = Depends(async_database.get_scoped_session)):
    device = await crud.get_device(session=session, device_id=device_id)
    if device:
        return device


@router.post("/", response_model=DevicesDTO)
async def create_device(device_in: DevicesCreateDTO,
                        session: AsyncSession = Depends(async_database.get_scoped_session)):
    return await crud.create_device(session=session, device_in=device_in)


@router.put("/{device_id}/")
async def update_device(
        device_update: DevicesUpdateDTO,
        device: Device = Depends(device_by_id),
        session: AsyncSession = Depends(async_database.get_scoped_session),
):
    return await crud.update_device(
        session=session,
        device=device,
        device_update=device_update,
    )


@router.patch("/{device_id}/")
async def update_device_partial(
        device_update: DevicesUpdatePartialDTO,
        device: Device = Depends(device_by_id),
        session: AsyncSession = Depends(async_database.get_scoped_session),
):
    return await crud.update_device(
        session=session,
        device=device,
        device_update=device_update,
        partial=True,
    )


@router.delete("/{device_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_device(
        device: Device = Depends(device_by_id),
        session: AsyncSession = Depends(async_database.get_scoped_session),
) -> None:
    await crud.delete_device(session=session, device=device)
