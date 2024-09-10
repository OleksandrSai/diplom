from aioredis import Redis


async def get_redis() -> Redis:
    return await Redis.from_url("redis://localhost")