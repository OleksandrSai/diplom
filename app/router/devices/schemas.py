from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from zigpy.profiles.zha import DeviceType


class DevicesBaseDTO(BaseModel):
    ieee: str
    name: Optional[str] = None
    type: DeviceType = Field(default=DeviceType(0x0000))
    nwk_adr: int

    model_config = ConfigDict(from_attributes=True)


class DevicesDTO(DevicesBaseDTO):
    id: int

    model_config = ConfigDict(from_attributes=True)


class DevicesCreateDTO(DevicesBaseDTO):
    pass


class DevicesUpdateDTO(DevicesCreateDTO):
    pass


class DevicesUpdatePartialDTO(DevicesCreateDTO):
    ieee: Optional[str] = None
    name: Optional[str] = None
    type: Optional[DeviceType] = None
    nwk_adr: Optional[int] = None


class DevicesResponse(BaseModel):
    items: list[DevicesDTO]
    totalItems: int
