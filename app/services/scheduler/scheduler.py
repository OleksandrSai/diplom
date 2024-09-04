from datetime import datetime, timedelta
from croniter import croniter
import calendar
from .orm import SchedulerOrm
import asyncio
import threading
from config import settings
from .smart_reader.smart_reader import SmartReader


class Scheduler:
    def __init__(self, controller):
        self.first_start = True
        self.time_first_start = settings.SCHEDULER_FIRST_POLL_SEC
        self.time_wait = settings.SCHEDULER_POLLING_RATE_SEC
        self.async_orm = SchedulerOrm()
        self.smart_reader = SmartReader(controller)
        self.data = None

    async def start(self):
        while True:
            try:
                await asyncio.sleep(self.time_wait)
                num_threads = threading.active_count()
                print(f"[Проверка]: Количество активных потоков: {num_threads}")
                if self.first_start:
                    await asyncio.sleep(self.time_first_start)
                    self.first_start = False
                    continue
                await self.data_waiter()
                await self.smart_reader.raed_all_devices()
            except Exception as e:
                print(e)

    async def data_waiter(self):
        self.data = await self.async_orm.get_all_scheduler()
        if self.data:
            await self.data_parser()

    async def data_parser(self):
        print(self.data)
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
                print("Hello")

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
