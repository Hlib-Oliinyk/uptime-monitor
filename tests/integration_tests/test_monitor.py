import pytest

from tests.data import TEST_MONITOR


@pytest.mark.asyncio
async def test_create_monitor_success(authorized_client):
    first_monitor = await authorized_client.post("/monitor/", json=TEST_MONITOR)
    second_monitor = await authorized_client.post("/monitor/", json=TEST_MONITOR)
    assert first_monitor.status_code == 200
    assert second_monitor.status_code == 200
    assert first_monitor.json()["user_id"] == 1


@pytest.mark.asyncio
async def test_get_monitor_success(authorized_client):
    response = await authorized_client.get("/monitor/1")
    assert response.status_code == 200
    assert response.json()["url"] == "https://example.com/"


@pytest.mark.asyncio
async def test_get_monitor_not_exist(authorized_client):
    response = await authorized_client.get("/monitor/999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_all_monitors(authorized_client):
    response = await authorized_client.get("/monitor/")
    assert response.status_code == 200
    assert len(response.json()) == 3


@pytest.mark.asyncio
async def test_update_monitor_success(authorized_client):
    response = await authorized_client.patch("/monitor/1", json={
        "url": "https://example.com/",
        "interval": 30,
        "is_active": "false"
    })
    assert response.json()["is_active"] == False


@pytest.mark.asyncio
async def test_update_monitor_not_authorized(async_client):
    response = await async_client.patch("/monitor/1", json={
        "url": "https://example.com/",
        "interval": 30,
        "is_active": "false"
    })
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_delete_monitor_success(authorized_client):
    response = await authorized_client.delete("/monitor/1")
    assert response.status_code == 200
    response = await authorized_client.get("/monitor/1")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_monitor_not_authorized(async_client):
    response = await async_client.delete("/monitor/1")
    assert response.status_code == 401

