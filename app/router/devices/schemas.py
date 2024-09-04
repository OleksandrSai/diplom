from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from zigpy.profiles.zha import DeviceType


class DevicesBaseDTO(BaseModel):
    ieee: str
    name: Optional[str] = None
    type: DeviceType = Field(default=DeviceType(0x0000))
    nwk_adr: int
    status: bool = Field(default=False)
    date_turn_on: Optional[datetime] = None
    date_turn_off: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class DevicesDTO(DevicesBaseDTO):
    id: int

    model_config = ConfigDict(from_attributes=True)


class DevicesCreateDTO(DevicesBaseDTO):
    pass


class DevicesUpdateDTO(DevicesCreateDTO):
    pass


class DevicesUpdatePartialDTO(DevicesCreateDTO):
    pass


class DevicesResponse(BaseModel):
    items: list[DevicesDTO]
    totalItems: int
