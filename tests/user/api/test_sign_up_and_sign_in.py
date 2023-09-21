import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_sign_up(api_client: AsyncClient, test_user_data: dict):
    response = await api_client.post("/user/sign-up", json=test_user_data)
    assert response.status_code == 201
    assert response.json() == {"message": "User Test is signed up!"}

@pytest.mark.asyncio
async def test_sign_up_if_user_exists(api_client: AsyncClient, test_user_data):
    response = await api_client.post("/user/sign-up", json=test_user_data)
    assert response.status_code == 409
    assert response.json() == {"message": "User with this phone or email already exists."}

@pytest.mark.asyncio
async def test_phone_validation(api_client: AsyncClient, test_user_data, monkeypatch):
    monkeypatch.setitem(test_user_data, "phone", "1")
    response = await api_client.post("/user/sign-up", json=test_user_data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Phone is invalid!"}

@pytest.mark.asyncio
async def test_email_validation(api_client: AsyncClient, test_user_data, monkeypatch):
    monkeypatch.setitem(test_user_data, "email", "email")
    response = await api_client.post("/user/sign-up", json=test_user_data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Email is invalid!"}

@pytest.mark.asyncio
async def test_unprocessable_entity(api_client: AsyncClient):
    with pytest.raises(AssertionError):
        response = await api_client.post("/user/sign-up", data={"name": "Test"})
        assert response.status_code == 200
        assert response.json() == {"name": "Test"}

@pytest.mark.asyncio
async def test_signin(api_client: AsyncClient, test_user_data):
    response = await api_client.post("/user/sign-in", json=test_user_data)
    assert response.status_code == 200
    assert response.json() == {"token": response.json().get("token")}

@pytest.mark.asyncio
async def test_signin_user_not_found(api_client: AsyncClient, test_user_data, monkeypatch):
    monkeypatch.setitem(test_user_data, "email", "email")
    response = await api_client.post("/user/sign-in", json=test_user_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found!"}

@pytest.mark.asyncio
async def test_signin_wrong_password(api_client: AsyncClient, test_user_data, monkeypatch):
    monkeypatch.setitem(test_user_data, "password", "1")
    response = await api_client.post("user/sign-in", json=test_user_data)
    assert response.status_code == 401
    assert response.json() == {"detail": "Wrong password!"}