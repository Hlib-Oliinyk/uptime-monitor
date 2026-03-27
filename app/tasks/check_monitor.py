import httpx
import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.celery import app
from app.core.config import settings
from app.repositories.check import CheckRepository
from app.repositories.monitor import MonitorRepository


def get_new_session():
    engine = create_async_engine(settings.DB_URL)
    return async_sessionmaker(engine, expire_on_commit=False)


async def check_monitor(monitor_id: int):
    async with get_new_session()() as db:
        monitor_repo = MonitorRepository(db)
        check_repo = CheckRepository(db)

        monitor = await monitor_repo.get_by_id(monitor_id)
        if monitor is None or not monitor.is_active:
            return

        async with httpx.AsyncClient(verify=False) as client:
            response = await client.get(monitor.url)

            response_time = response.elapsed.total_seconds()
            status_code = response.status_code

            check_dict = {
                "monitor_id": monitor_id,
                "status_code": status_code,
                "response_time": response_time,
            }

            await check_repo.create(**check_dict)

    return monitor.interval


@app.task
def check_monitor_task(monitor_id: int):
    coro = check_monitor(monitor_id)
    interval = asyncio.run(coro)

    if interval is not None:
        check_monitor_task.apply_async(args=[monitor_id], countdown=interval)