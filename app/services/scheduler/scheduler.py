from datetime import datetime, timedelta
from croniter import croniter
import calendar
from .orm import SchedulerOrm


class Scheduler:
    def __init__(self, **kwargs):
        self.async_orm = SchedulerOrm()

    async def data_waiter(self):
        self.data = await self.async_orm.get_all_scheduler_with_name()
        if self.data:
            await self.data_parser()

    async def data_parser(self):
        for key in self.data:
            group_id = key['group_id']
            cron_id = key['id']
            cron_str = key['cron_str']
            pause = key['pause']
            last_poll_time = key['last_poll']
            if 'L-1' in cron_str or 'L-2' in cron_str:
                last_day_of_month = calendar.monthrange(last_poll_time.year, last_poll_time.month)[1]

                if 'L-1' in cron_str:
                    cron_str = cron_str.replace('L-1', str(last_day_of_month))

                if 'L-2' in cron_str:
                    cron_str = cron_str.replace('L-2', str(last_day_of_month - 1))

            cron = croniter(cron_str, last_poll_time)
            next_cron_time = cron.get_next(datetime)
            current_time = datetime.now()

            if Scheduler.is_interval_cron(key['cron_str']):
                number = Scheduler.extract_interval(key['cron_str'])
                next_cron_time = last_poll_time + timedelta(minutes=number)

            if next_cron_time <= current_time:
                GroupReader(group_id, cron_id, current_time, pause)

    @staticmethod
    def is_interval_cron(cron_expression):
        parts = cron_expression.split()
        if not parts[0].startswith('*/'):
            return False
        for part in parts[1:]:
            if part != '*' and not part.isdigit():
                return False
        return True

    @staticmethod
    def extract_interval(cron_expression):
        interval_str = cron_expression.split()[0]
        interval = int(interval_str[2:])
        return interval
