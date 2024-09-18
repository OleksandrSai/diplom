from aioredis import Redis
from sqlalchemy import select, func
from sqlalchemy.engine import Result


async def get_redis() -> Redis:
    return await Redis.from_url("redis://localhost")


async def get_data(session, base_query, limit, offset):
    total_items, result, data = None, None, None

    if limit:
        subquery = base_query.subquery()
        count_query = select(func.count()).select_from(subquery)
        paginated_query = base_query.offset(offset).limit(limit)
        total_items_result = await session.execute(count_query)
        total_items = total_items_result.scalar()
        result: Result = await session.execute(paginated_query)
    else:
        result: Result = await session.execute(base_query)

    data = result.scalars().all()

    if limit:
        return list(data), total_items
    else:
        return list(data)
