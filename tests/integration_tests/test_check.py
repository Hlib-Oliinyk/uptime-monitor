import pytest


@pytest.mark.asyncio
async def test_get_all_checks(authorized_client, test_check):
    response = await authorized_client.get(f"/check/{test_check.monitor_id}")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_monitor_stats(authorized_client):
    response = await authorized_client.get("/check/1/stats")
    assert response.status_code == 200
    assert response.json()["uptime_percentage"] == 100
    assert response.json()["total_checks"] == 1


@pytest.mark.asyncio
async def test_get_monitor_stats_not_exist(authorized_client):
    response = await authorized_client.get("/check/2/stats")
    assert response.status_code == 404