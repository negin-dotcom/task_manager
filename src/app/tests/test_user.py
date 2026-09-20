import pytest
from sqlalchemy import select

from app.db.models.user import User
from app.tests.conftest import TestSessionLocal 


class TestUserRegistration:

    # Run this test asynchronously.
    @pytest.mark.anyio
    async def test_create_user(self, client):
        data = {
            "username": "testuser",
            "password": "testpassword123",
            "email": "test@example.com"
        }

        response = await client.post(
            "/users",
            json=data
        ) 

        assert response.status_code == 201

        data = response.json()

        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"
        assert "password" not in data

    @pytest.mark.anyio
    async def test_duplicate_username(self, client):
        data = {
            "username": "testuser",
            "password": "testpassword123",
            "email": "test@example.com"
        }

        response = await client.post("/users", json=data)

        assert response.status_code == 201 

        data["email"] = "another@example.com"
        response = await client.post("/users", json=data)

        assert response.status_code == 409
        assert response.json()["detail"] == "Username already exists."

    @pytest.mark.anyio
    async def test_duplicate_email(self, client):
        data = {
            "username": "testuser",
            "password": "testpassword123",
            "email": "test@example.com"
        }

        response = await client.post("/users", json=data)

        assert response.status_code == 201 

        data["username"] = "another_testuser"
        response = await client.post("/users", json=data)

        assert response.status_code == 409
        assert response.json()["detail"] == "Email already exists."

    @pytest.mark.anyio
    async def test_missing_username(self, client):
        data = {
            "password": "testpassword123",
            "email": "test@example.com"
        }

        response = await client.post("/users", json=data)

        assert response.status_code == 422
         
    @pytest.mark.anyio
    async def test_missing_password(self, client):
        data = {
            "username": "testuser",
            "email": "test@example.com"
        }

        response = await client.post("/users", json=data)

        assert response.status_code == 422 

    @pytest.mark.anyio
    async def test_missing_email(self, client):
        data = {
            "username": "testuser",
            "password": "testpassword123",
        }

        response = await client.post("/users", json=data)

        assert response.status_code == 422 

    @pytest.mark.anyio
    async def test_invalid_email(self, client):
        data = {
            "username": "testuser",
            "password": "testpassword123",
            "email": "example"
        }

        response = await client.post(
            "/users",
            json=data
        ) 

        assert response.status_code == 422 

    @pytest.mark.anyio
    async def test_empty_request(self, client):
        data = {}

        response = await client.post("/users", json=data)

        assert response.status_code == 422

    @pytest.mark.anyio
    async def test_short_password(self, client):
        data = {
            "username": "testuser",
            "password": "pass",
            "email": "test@example.com"
        }

        response = await client.post(
            "/users",
            json=data
        ) 

        assert response.status_code == 422 

    @pytest.mark.anyio
    async def test_long_password(self, client):
        data = {
            "username": "testuser",
            "password": "h" * 129,
            "email": "test@example.com"
        }

        response = await client.post(
            "/users",
            json=data
        ) 

        assert response.status_code == 422 

    @pytest.mark.anyio
    async def test_short_username(self, client):
        data = {
            "username": "u",
            "password": "testpass123",
            "email": "test@example.com"
        }

        response = await client.post(
            "/users",
            json=data
        ) 

        assert response.status_code == 422 

    @pytest.mark.anyio
    async def test_long_username(self, client):
        data = {
            "username": "u" * 51,
            "password": "testpass123",
            "email": "test@example.com"
        }

        response = await client.post(
            "/users",
            json=data
        ) 

        assert response.status_code == 422 


    @pytest.mark.anyio
    async def test_hashed_password(self, client):
        data = {
            "username": "testuser",
            "password": "testpass123",
            "email": "test@example.com"
        }

        response = await client.post(
            "/users",
            json=data
        ) 

        assert response.status_code == 201

        async with TestSessionLocal() as db:
            result = await db.execute(
                select(User)
                .where(User.username == response.json()["username"])
            ) 

            user = result.scalar_one_or_none()

            assert user.password != "testpass123"