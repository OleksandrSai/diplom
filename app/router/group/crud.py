from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result
from app.core.models import Group
from .schemas import GroupCreateDTO, GroupUpdatePartialDTO, GroupUpdateDTO


async def get_groups(session: AsyncSession) -> list[Group]:
    stmt = select(Group).order_by(Group.id)
    result: Result = await session.execute(stmt)
    groups = result.scalars().all()
    return list(groups)


async def get_group(session: AsyncSession, group_id: int) -> Group | None:
    return await session.get(Group, group_id)


async def create_group(session: AsyncSession, group_in: GroupCreateDTO) -> Group | None:
    group = Group(**group_in.model_dump())
    session.add(group)
    await session.commit()
    return group


async def update_group(session: AsyncSession,
                       group_update: GroupUpdatePartialDTO | GroupUpdateDTO,
                       group: Group,
                       partial: bool = False) -> Group:
    for key, value in group_update.model_dump(exclude_unset=partial).items():
        setattr(group, key, value)
    await session.commit()
    return group


async def delete_group(session: AsyncSession, group: Group) -> None:
    await session.delete(group)
    await session.commit()
