from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class StatisticBaseDTO(BaseModel):
    device_id: int
    instant_current: float
    instant_voltage: float
    total_consumption: float
    created_at: Optional[datetime] = datetime.utcnow()

    model_config = ConfigDict(from_attributes=True)


class StatisticDTO(StatisticBaseDTO):
    id: int

    model_config = ConfigDict(from_attributes=True)


class StatisticCreateDTO(StatisticBaseDTO):
    pass


class StatisticResponse(BaseModel):
    items: list[StatisticDTO]
    totalItems: int
