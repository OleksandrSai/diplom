from app.core.async_database import async_session_factory
from app.router.scheduler import crud
from app.router.scheduler.schemas import SchedulerDTO
from app.core.models import Scheduler


class SchedulerOrm:

    @staticmethod
    async def get_all_scheduler() -> list:
        async with async_session_factory as session:
            scheduler: list[Scheduler] = await crud.get_schedulers(session=session)
            return [SchedulerDTO.model_validate(row).model_dump() for row in scheduler]
