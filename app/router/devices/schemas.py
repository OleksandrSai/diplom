from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional
from zigpy.profiles.zha import DeviceType


class DevicesBaseDTO(BaseModel):
    address: str
    name: str
    type: DeviceType
    nwk_adr: str
    status: bool
    date_turn_on: Optional[datetime]
    date_turn_off: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class DevicesDTO(DevicesBaseDTO):
    id: int


class DevicesCreateDTO(DevicesBaseDTO):
    pass


class DevicesUpdateDTO(DevicesCreateDTO):
    pass


class DevicesUpdatePartialDTO(DevicesCreateDTO):
    pass


class DevicesResponse(BaseModel):
    items: list[DevicesDTO]
    totalItems: int
