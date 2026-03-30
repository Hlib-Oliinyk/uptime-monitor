import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.celery import app
from app.core.config import settings
from app.repositories.monitor import MonitorRepository
from app.tasks.check_monitor import check_monitor_task


def get_new_session():
    engine = create_async_engine(settings.DB_URL)
    return async_sessionmaker(engine, expire_on_commit=False)


async def get_active_monitors():
    async with get_new_session()() as db:
        monitor_repo = MonitorRepository(db)
        active_monitors = await monitor_repo.get_active_monitors()

    return active_monitors


@app.task
def restart_active_monitors_task():
    coro = get_active_monitors()
    active_monitors = asyncio.run(coro)

    for monitor in active_monitors:
        check_monitor_task.delay(monitor.id)