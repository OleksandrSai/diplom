from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, func
from app.core.models import Device
from .schemas import DevicesCreateDTO, DevicesUpdatePartialDTO, DevicesUpdateDTO


async def get_devices(session: AsyncSession, offset: int = 0, limit: int = 10, search: str = "") -> (
        tuple[list[Device], int]):
    base_query = select(Device).order_by(Device.id)

    if search:
        search_pattern = f"%{search}%"
        base_query = base_query.where(
            or_(
                Device.name.ilike(search_pattern)
            )
        )

    subquery = base_query.subquery()
    count_query = select(func.count()).select_from(subquery)

    paginated_query = base_query.offset(offset).limit(limit)

    result = await session.execute(paginated_query)
    devices = result.scalars().all()

    total_items_result = await session.execute(count_query)
    total_items = total_items_result.scalar()

    return list(devices), total_items


async def get_device(session: AsyncSession, device_id: int) -> Device | None:
    return await session.get(Device, device_id)


async def create_device(session: AsyncSession, device_in: DevicesCreateDTO) -> Device | None:
    device = Device(**device_in.model_dump())
    session.add(device)
    await session.commit()
    return device


async def update_device(session: AsyncSession,
                        device_update: DevicesUpdatePartialDTO | DevicesUpdateDTO,
                        device: Device,
                        partial: bool = False) -> Device:
    for key, value in device_update.model_dump(exclude_unset=partial).items():
        setattr(device, key, value)
    await session.commit()
    return device


async def delete_device(session: AsyncSession, device: Device) -> None:
    await session.delete(device)
    await session.commit()
