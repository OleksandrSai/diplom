from fastapi import APIRouter, Depends, status
from . import crud
from .schemas import GroupCreateDTO, GroupUpdateDTO, GroupUpdatePartialDTO, GroupDTO
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.async_database import async_database
from .dependencies import group_by_id
from app.core.models import Group

router = APIRouter(tags=["group"])


@router.get("/", response_model=list[GroupDTO])
async def get_groups(session: AsyncSession = Depends(async_database.get_scoped_session)):
    return await crud.get_groups(session=session)


@router.get("/{group_id}/", response_model=GroupDTO)
async def create_group(group_id: int, session: AsyncSession = Depends(async_database.get_scoped_session)):
    group = await crud.get_group(session=session, group_id=group_id)
    if group:
        return group


@router.post("/", response_model=GroupDTO)
async def create_group(group_in: GroupCreateDTO,
                       session: AsyncSession = Depends(async_database.get_scoped_session)):
    return await crud.create_group(session=session, group_in=group_in)


@router.put("/{group_id}/")
async def update_group(
        group_update: GroupUpdateDTO,
        group: Group = Depends(group_by_id),
        session: AsyncSession = Depends(async_database.get_scoped_session),
):
    return await crud.update_group(
        session=session,
        group=group,
        group_update=group_update,
    )


@router.patch("/{group_id}/")
async def update_group_partial(
        group_update: GroupUpdatePartialDTO,
        group: Group = Depends(group_by_id),
        session: AsyncSession = Depends(async_database.get_scoped_session),
):
    return await crud.update_group(
        session=session,
        group=group,
        group_update=group_update,
        partial=True,
    )


@router.delete("/{group_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_scheduler(
        group: Group = Depends(group_by_id),
        session: AsyncSession = Depends(async_database.get_scoped_session),
) -> None:
    await crud.delete_group(session=session, group=group)
