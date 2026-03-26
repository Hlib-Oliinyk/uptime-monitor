import httpx
import asyncio

from app.celery import app
from app.db.database import AsyncSessionLocal
from app.repositories.check import CheckRepository
from app.repositories.monitor import MonitorRepository


async def check_monitor(monitor_id: int):
    async with AsyncSessionLocal() as db:
        monitor_repo = MonitorRepository(db)
        check_repo = CheckRepository(db)

        monitor = await monitor_repo.get_by_id(monitor_id)
        if not monitor.is_active or monitor is None:
            return

        async with httpx.AsyncClient() as client:
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
    check_monitor_task.apply_async(args=[monitor_id], countdown=interval)
