from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
    AsyncSession
)

from config import settings
from sqlalchemy.pool import NullPool


class AsyncDatabase:
    def __init__(self, url: str, echo: bool = False):
        self.url = url
        self.echo = echo
        self.engine = create_async_engine(
            url=url,
            echo=echo,
            poolclass=NullPool
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            expire_on_commit=True,
        )

    def get_session_factory(self):
        return self.session_factory()

    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

    async def session_dependency(self) -> AsyncSession:
        async with self.session_factory() as session:
            try:
                yield session
            finally:
                await session.close()


async_database = AsyncDatabase(
    url=settings.DATABASE_URL_pymysql,
    echo=False,
)

async_session_factory = async_database.get_session_factory()
