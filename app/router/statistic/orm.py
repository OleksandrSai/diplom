from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.models import Statistic
from app.utils.dependencies import get_data
from app.utils.orm import utils
from datetime import datetime, time, timedelta
from sqlalchemy import and_
from sqlalchemy.engine import Result


async def get_statistic_by_device_id(session: AsyncSession, device_id: int, offset: int = 0, limit: int = 0) -> (
        tuple[list[Statistic], int]):
    base_query = select(Statistic).filter_by(device_id=device_id)
    return await get_data(session=session, base_query=base_query, limit=limit, offset=offset)


async def get_statistic_trend_by_date(session: AsyncSession,
                                      device_id: int = 5,
                                      date_range: str = '2024-09-15T00:24:46, 2024-09-15T23:24:46'):
    date_range = date_range.split(',')
    start_date = utils.parse_iso_date(date_range[0])
    end_date = utils.parse_iso_date(date_range[1])

    start_datetime = datetime.combine(start_date, time.min) - timedelta(microseconds=1)
    end_datetime = datetime.combine(end_date, time.max) + timedelta(microseconds=1)

    base_query = select(Statistic).filter_by(device_id=device_id)
    base_query = base_query.filter(
        and_(
            Statistic.created_at >= start_datetime,
            Statistic.created_at <= end_datetime
        )
    ).order_by(Statistic.created_at)

    res: Result = await session.execute(base_query)
    statistics = res.scalars().all()

    if start_date.date() == end_date.date():
        hourly_consumption = {}

        for stat in statistics:
            hour = stat.created_at.strftime('%H:00')
            if hour not in hourly_consumption:
                hourly_consumption[hour] = {
                    "start_value": stat.total_consumption,
                    "end_value": stat.total_consumption
                }
            else:
                hourly_consumption[hour]["end_value"] = stat.total_consumption

        consumption_per_hour = {}
        for hour, values in hourly_consumption.items():
            consumption_per_hour[hour] = values["end_value"] - values["start_value"]

        return consumption_per_hour

    else:
        daily_consumption = {}

        for stat in statistics:
            day = stat.created_at.date()
            if day not in daily_consumption:
                daily_consumption[day] = {
                    "start_value": stat.total_consumption,
                    "end_value": stat.total_consumption
                }
            else:
                daily_consumption[day]["end_value"] = stat.total_consumption

        consumption_per_day = {}
        for day, values in daily_consumption.items():
            consumption_per_day[day] = values["end_value"] - values["start_value"]

        return consumption_per_day
