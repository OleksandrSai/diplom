import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, text, Boolean
from .base import Base, str_256
from zigpy.profiles.zha import DeviceType
from app.utils.enum import Strategy
from typing import Optional, Annotated

created_at = Annotated[datetime.datetime, mapped_column(server_default=text("NOW()"))]
update = Annotated[datetime.datetime, mapped_column(server_default=text("NOW()"), onupdate=text("NOW()"))]


class Device(Base):
    address: Mapped[str_256]
    name: Mapped[str_256]
    type: Mapped[DeviceType]
    nwk_adr: Mapped[str_256]
    status: Mapped[bool]
    date_turn_on: Mapped[Optional[datetime.datetime]]
    date_turn_off: Mapped[Optional[datetime.datetime]]


class Group(Base):
    name: Mapped[str_256]
    strategy: Mapped[Strategy]
    value_strategy: Mapped[Optional[int]]


class GroupDevicePriority(Base):
    group_id: Mapped[int] = mapped_column(ForeignKey("group.id", ondelete="CASCADE"))
    device_id: Mapped[int] = mapped_column(ForeignKey("device.id", ondelete="CASCADE"))
    priority: Mapped[int]


class Statistic(Base):
    device_id: Mapped[int] = mapped_column(ForeignKey("device.id", ondelete="CASCADE"))
    instant_current: Mapped[float]
    instant_voltage: Mapped[float]
    total_consumption: Mapped[float]
    created_at: Mapped[created_at]


class Scheduler(Base):
    group_id: Mapped[int] = mapped_column(ForeignKey("group.id", ondelete="CASCADE"))
    pause: Mapped[bool] = mapped_column(Boolean, default=False)
    cron_str: Mapped[str_256]
    last_poll: Mapped[update]
