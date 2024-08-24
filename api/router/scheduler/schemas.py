import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional


class SchedulerBaseDTO(BaseModel):
    group_id: int
    pause: bool
    cron_str: str
    last_poll: Optional[datetime.datetime]


class SchedulerDTO(SchedulerBaseDTO):
    model_config = ConfigDict(from_attributes=True)
    id: int


class SchedulerCreateDTO(SchedulerBaseDTO):
    pass
