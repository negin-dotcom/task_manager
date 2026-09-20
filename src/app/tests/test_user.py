from datetime import datetime, timezone

import pytest
from sqlalchemy import select

from app.db.models.user import User
from app.tests.conftest import TestSessionLocal 

from app.core.security import create_access_token, decode_access_token, verify_password

from jose import jwt
from app.core.config import settings


class TestUserRegistration:
    """Tests whether users can register successfully."""

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

            assert user is not None
            assert user.password != "testpass123"
            assert verify_password("testpass123", user.password)

    @pytest.mark.anyio
    async def test_username_min_length(self, client):
        data = {
            "username": "u" * 3,
            "password": "testpass123",
            "email": "test@example.com"
        }

        response = await client.post(
            "/users",
            json=data
        ) 

        assert response.status_code == 201

    @pytest.mark.anyio
    async def test_username_max_length(self, client):
        data = {
            "username": "u" * 50,
            "password": "testpass123",
            "email": "test@example.com"
        }

        response = await client.post(
            "/users",
            json=data
        ) 

        assert response.status_code == 201

    @pytest.mark.anyio
    async def test_password_min_length(self, client):
        data = {
            "username": "testuser",
            "password": "p" * 8,
            "email": "test@example.com"
        }

        response = await client.post(
            "/users",
            json=data
        ) 

        assert response.status_code == 201

    @pytest.mark.anyio
    async def test_password_max_length(self, client):
        data = {
            "username": "testuser",
            "password": "p" * 128,
            "email": "test@example.com"
        }

        response = await client.post(
            "/users",
            json=data
        ) 

        assert response.status_code == 201



class TestUserLogin:
    """Tests whether users can authenticate successfully."""

    @pytest.mark.anyio
    async def test_login_success(self, client):
        data = {
            "username": "testuser",
            "password": "testpass123",
            "email": "test@example.com"
        }

        response = await client.post("/users", json=data)

        assert response.status_code == 201

        user_data = response.json()

        login_data = {
            "username": user_data["username"],
            "password": "testpass123"
        }

        # Because of oauth, `data` is used rather than `json`.
        response = await client.post("/auth/login", data=login_data)

        assert response.status_code == 200

        response_data = response.json()

        assert "access_token" in response_data
        assert response_data["token_type"] == "bearer"

        payload = decode_access_token(token=response_data["access_token"])

        assert "exp" in payload
        assert payload["sub"] == str(user_data["id"])

    @pytest.mark.anyio
    async def test_user_cannot_login_with_wrong_password(self, client):
        data = {
            "username": "testuser",
            "password": "testpass123",
            "email": "test@example.com"
        }

        response = await client.post("/users", json=data)

        assert response.status_code == 201

        login_data = {
            "username": response.json()["username"],
            "password": "new_pass"
        }

        response = await client.post("/auth/login", data=login_data)
        
        assert response.status_code == 401
        
    @pytest.mark.anyio
    async def test_user_cannot_login_with_nonexistent_username(self, client):
        data = {
            "username": "testuser",
            "password": "testpass123",
            "email": "test@example.com"
        }

        response = await client.post("/users", json=data)

        assert response.status_code == 201

        login_data = {
            "username": "new_testuser",
            "password": "testpass123"
        }

        response = await client.post("/auth/login", data=login_data)
                
        assert response.status_code == 401

    @pytest.mark.anyio
    async def test_user_cannot_login_with_missing_username(self, client):
        data = {
            "username": "testuser",
            "password": "testpass123",
            "email": "test@example.com"
        }

        response = await client.post("/users", json=data)

        assert response.status_code == 201

        login_data = {
            "password": "testpass123"
        }

        response = await client.post("/auth/login", data=login_data)
                
        assert response.status_code == 422

    @pytest.mark.anyio
    async def test_user_cannot_login_with_missing_password(self, client):
        data = {
            "username": "testuser",
            "password": "testpass123",
            "email": "test@example.com"
        }

        response = await client.post("/users", json=data)

        assert response.status_code == 201

        login_data = {
            "username": "testuser"
        }

        response = await client.post("/auth/login", data=login_data)
                
        assert response.status_code == 422

    @pytest.mark.anyio
    async def test_user_cannot_login_with_empty_request(self, client):
        data = {
            "username": "testuser",
            "password": "testpass123",
            "email": "test@example.com"
        }

        response = await client.post("/users", json=data)

        assert response.status_code == 201

        login_data = {}

        response = await client.post("/auth/login", data=login_data)

        assert response.status_code == 422


class TestJWTAuthorization:
    """Tests whether the application correctly use JWTs to protect endpoints."""

    @pytest.mark.anyio
    async def test_access_protected_endpoint_with_valid_jwt(self, client):
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

        login_data = {
            "username": response.json()["username"],
            "password": "testpass123"
        }

        response = await client.post("/auth/login", data=login_data)

        assert response.status_code == 200

        access_token = response.json()["access_token"]
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        response = await client.get("/users/me", headers=headers)

        assert response.status_code == 200

    @pytest.mark.anyio
    async def test_access_protected_endpoint_without_jwt(self, client):
        response = await client.get("/users/me")

        assert response.status_code == 401

    @pytest.mark.anyio
    async def test_access_protected_endpoint_with_invalid_jwt(self, client):
        headers = {
            "Authorization": "Bearer test_invalid_jwt"
        }
        response = await client.get("/users/me", headers=headers)

        assert response.status_code == 401

    @pytest.mark.anyio
    async def test_access_protected_endpoint_with_expired_jwt(self, client):
        payload = {
            "sub": "1",
            "exp": int(datetime.now(timezone.utc).timestamp()) - 60   # 60 seconds ago
        }

        token = jwt.encode(
            payload,
            settings.jwt_secret_key,
            algorithm=settings.jwt_algorithm
        )

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = await client.get("/users/me", headers=headers)

        assert response.status_code == 401

    @pytest.mark.anyio
    async def test_access_protected_endpoint_with_wrong_jwt_secret(self, client):
        payload = {
            "sub": "1",
            "exp": int(datetime.now(timezone.utc).timestamp()) + 60
        }

        token = jwt.encode(
            payload,
            "some_secret_key",
            algorithm=settings.jwt_algorithm
        )

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = await client.get("/users/me", headers=headers)

        assert response.status_code == 401

    @pytest.mark.anyio
    async def test_access_protected_endpoint_for_nonexistent_user(self, client):
        payload = {
            "sub": "999999",
            "exp": int(datetime.now(timezone.utc).timestamp()) + 60
        }

        token = jwt.encode(
            payload,
            settings.jwt_secret_key,
            algorithm=settings.jwt_algorithm
        )

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = await client.get("/users/me", headers=headers)

        assert response.status_code == 401

    @pytest.mark.anyio
    async def test_access_protected_endpoint_with_missing_sub_in_jwt(self, client):
        payload = {
            "exp": int(datetime.now(timezone.utc).timestamp()) + 60
        }

        token = jwt.encode(
            payload,
            settings.jwt_secret_key,
            algorithm=settings.jwt_algorithm
        )

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = await client.get("/users/me", headers=headers)

        assert response.status_code == 401

    @pytest.mark.anyio
    async def test_access_protected_endpoint_with_invalid_sub_in_jwt(self, client):
        payload = {
            "sub": "a",
            "exp": int(datetime.now(timezone.utc).timestamp()) + 60
        }

        token = jwt.encode(
            payload,
            settings.jwt_secret_key,
            algorithm=settings.jwt_algorithm
        )

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = await client.get("/users/me", headers=headers)

        assert response.status_code == 401

    @pytest.mark.anyio
    async def test_access_protected_endpoint_without_exp_in_jwt(self, client):
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

        payload = {
            "sub": str(response.json()["id"]),
        }

        token = jwt.encode(
            payload,
            settings.jwt_secret_key,
            algorithm=settings.jwt_algorithm
        )

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = await client.get("/users/me", headers=headers)

        assert response.status_code == 401