import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.celery import app
from app.core.config import settings
from app.repositories.check import CheckRepository


def get_new_session():
    engine = create_async_engine(settings.DB_URL)
    return async_sessionmaker(engine, expire_on_commit=False)


async def cleanup_old_checks():
    async with get_new_session()() as db:
        check_repo = CheckRepository(db)
        await check_repo.delete_inactive_checks()


@app.task
def cleanup_old_checks_task():
    coro = cleanup_old_checks()
    asyncio.run(coro)