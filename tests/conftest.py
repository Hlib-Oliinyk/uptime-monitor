import pytest_asyncio

from httpx import AsyncClient, ASGITransport

from app.main import app
from app.models.check import Check
from app.dependencies import get_db
from app.models.monitor import Monitor
from app.db.database import Base, AsyncSessionTest, test_async_engine
from tests.data import (
    TEST_USER,
    TEST_LOGIN,
    TEST_MONITOR,
    TEST_CHECK
)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_db():
    async with test_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def override_get_db():
    async with AsyncSessionTest() as db:
        yield db


@pytest_asyncio.fixture(scope="session", autouse=True)
async def override_dependencies():
    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def db_session():
    async with AsyncSessionTest() as db:
        yield db
        await db.rollback()


@pytest_asyncio.fixture(autouse=True)
async def mock_celery_task(mocker):
    mocker.patch("app.tasks.check_monitor.check_monitor_task.delay")


@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client


@pytest_asyncio.fixture
async def authorized_client(async_client):
    await async_client.post("/auth/register", json=TEST_USER)
    response = await async_client.post('/auth/login', json=TEST_LOGIN)
    assert response.status_code == 200
    return async_client


@pytest_asyncio.fixture
async def test_monitor(db_session):
    monitor_dict = TEST_MONITOR
    monitor_dict["user_id"] = 1
    monitor = Monitor(**TEST_MONITOR)

    db_session.add(monitor)
    await db_session.commit()
    await db_session.refresh(monitor)
    return monitor


@pytest_asyncio.fixture
async def test_check(db_session, test_monitor):
    check = Check(**TEST_CHECK)
    db_session.add(check)
    await db_session.commit()
    await db_session.refresh(check)
    return check