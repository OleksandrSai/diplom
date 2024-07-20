from sqlalchemy.orm import Mapped
from .base import Base
from zigpy.profiles.zha import DeviceType


class Device(Base):
    address: Mapped[str]
    type: Mapped[DeviceType]
