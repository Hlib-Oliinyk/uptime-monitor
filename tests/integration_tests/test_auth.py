import pytest

from tests.data import TEST_USER, TEST_LOGIN


@pytest.mark.asyncio
async def test_register_success(async_client):
    response = await async_client.post("/auth/register", json=TEST_USER)
    assert response.status_code == 200
    assert response.json()["username"] == "test"


@pytest.mark.asyncio
async def test_register_user_exist(async_client):
    response = await async_client.post("/auth/register", json=TEST_USER)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_login_success(async_client):
    response = await async_client.post("/auth/login", json=TEST_LOGIN)
    assert response.status_code == 200
    assert "access_token" in response.cookies
    assert "refresh_token" in response.cookies


@pytest.mark.asyncio
async def test_login_wrong_password(async_client):
    response = await async_client.post("/auth/login", json={
        "email": "test@gmail.com",
        "password": "wrong-password"
    })
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_logout(authorized_client):
    response = await authorized_client.delete("/auth/logout")
    assert response.status_code == 200
    assert "access_token" not in response.cookies
    assert "refresh_token" not in response.cookies


@pytest.mark.asyncio
async def test_refresh(async_client):
    first_response = await async_client.post("/auth/login", json=TEST_LOGIN)
    first_refresh = first_response.json()["refresh_token"]
    second_response = await async_client.post("/auth/refresh")
    second_refresh = second_response.json()["refresh_token"]
    assert first_refresh != second_refresh