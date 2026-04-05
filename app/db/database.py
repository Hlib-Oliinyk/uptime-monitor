from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


async_engine = create_async_engine(
    settings.DB_URL,
    echo = False
)

test_async_engine = create_async_engine(
    settings.TEST_DB_URL,
    echo = False
)


AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit = False)
AsyncSessionTest = async_sessionmaker(test_async_engine, expire_on_commit = False)


class Base(DeclarativeBase):
    pass