import pytest 


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