import pytest 


class TestTasks:

    @pytest.mark.anyio
    async def test_create_task(self, client):
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

        user_data = response.json()

        login_data = {
            "username": user_data["username"],
            "password": "testpassword123"
        }

        response = await client.post("/auth/login", data=login_data)
        
        assert response.status_code == 200
        response_data = response.json()

        assert "access_token" in response_data
        assert response_data["token_type"] == "bearer"

        access_token = response_data["access_token"]
        task_data = {
            "title": "Test Title",
        }
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = await client.post("/tasks", json=task_data, headers=headers)
        
        assert response.status_code == 201
        created_task_data = response.json()

        assert created_task_data["title"] == "Test Title"
        assert "created_at" in created_task_data

    @pytest.mark.anyio
    async def test_get_task(self, client):
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

        user_data = response.json()

        login_data = {
            "username": user_data["username"],
            "password": "testpassword123"
        }

        response = await client.post("/auth/login", data=login_data)
        
        assert response.status_code == 200
        response_data = response.json()

        assert "access_token" in response_data
        assert response_data["token_type"] == "bearer"

        access_token = response_data["access_token"]
        task_data = {
            "title": "Test Title",
        }
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = await client.post("/tasks", json=task_data, headers=headers)
        
        assert response.status_code == 201
        created_task_data = response.json()

        response = await client.get(f"/tasks/{created_task_data['id']}", 
                                    headers=headers)

        assert response.status_code == 200
        retrieved_task_data = response.json()

        assert retrieved_task_data["title"] == "Test Title"
        assert retrieved_task_data["id"] == created_task_data["id"]

    @pytest.mark.anyio
    async def test_get_task_without_jwt(self, client):
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

        user_data = response.json()

        login_data = {
            "username": user_data["username"],
            "password": "testpassword123"
        }

        response = await client.post("/auth/login", data=login_data)
        
        assert response.status_code == 200
        response_data = response.json()

        assert "access_token" in response_data
        assert response_data["token_type"] == "bearer"

        access_token = response_data["access_token"]
        task_data = {
            "title": "Test Title",
        }
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = await client.post("/tasks", json=task_data, headers=headers)
        
        assert response.status_code == 201
        created_task_data = response.json()

        response = await client.get(f"/tasks/{created_task_data['id']}")

        assert response.status_code == 401

    @pytest.mark.anyio
    async def test_get_task_with_nonexistent_task(self, client):
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

        user_data = response.json()

        login_data = {
            "username": user_data["username"],
            "password": "testpassword123"
        }

        response = await client.post("/auth/login", data=login_data)
        
        assert response.status_code == 200
        response_data = response.json()

        assert "access_token" in response_data
        assert response_data["token_type"] == "bearer"

        access_token = response_data["access_token"]
        task_data = {
            "title": "Test Title",
        }
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = await client.post("/tasks", json=task_data, headers=headers)
        
        assert response.status_code == 201
        nonexistent_task_id = 999999

        response = await client.get(f"/tasks/{nonexistent_task_id}",
                                    headers=headers)

        assert response.status_code == 404

    @pytest.mark.anyio
    async def test_get_task_belonging_to_another_user(self, client):
        # --------- User 1 --------
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

        user_data = response.json()

        login_data = {
            "username": user_data["username"],
            "password": "testpassword123"
        }

        response = await client.post("/auth/login", data=login_data)
        
        assert response.status_code == 200
        response_data = response.json()
        user_1_access_token = response_data["access_token"]

        task_data = {
            "title": "Test Title",
        }
        headers = {
            "Authorization": f"Bearer {user_1_access_token}"
        }
        response = await client.post("/tasks", json=task_data, headers=headers)
        assert response.status_code == 201
        created_task_data = response.json()

        # ------- User 2 ------------
        data_2 = {
            "username": "testuser_2",
            "password": "testpassword123",
            "email": "test2@example.com"
        }

        response = await client.post(
            "/users",
            json=data_2
        ) 

        assert response.status_code == 201

        user_2_data = response.json()

        login_2_data = {
            "username": user_2_data["username"],
            "password": "testpassword123"
        }

        response = await client.post("/auth/login", data=login_2_data)
        
        assert response.status_code == 200
        response_2_data = response.json()
        user_2_access_token = response_2_data["access_token"]

        headers_2 = {
            "Authorization": f"Bearer {user_2_access_token}"
        }

        response = await client.get(f"/tasks/{created_task_data['id']}",
                                    headers=headers_2)
                
        assert response.status_code == 404

    @pytest.mark.anyio
    async def test_get_all_tasks(self, client):
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

        user_data = response.json()

        login_data = {
            "username": user_data["username"],
            "password": "testpassword123"
        }

        response = await client.post("/auth/login", data=login_data)
        
        assert response.status_code == 200
        response_data = response.json()
        access_token = response_data["access_token"]

        task_1_data = {
            "title": "Test Title 1",
        }

        task_2_data = {
            "title": "Test Title 2",
        }

        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        response = await client.post("/tasks",
                                      json=task_1_data, 
                                      headers=headers)
        assert response.status_code == 201

        response = await client.post("/tasks",
                                     json=task_2_data, 
                                     headers=headers)
        assert response.status_code == 201

        response = await client.get("/tasks",
                                    headers=headers)

        assert response.status_code == 200
        response_data = response.json()

        assert len(response_data) == 2

        titles = {task["title"] for task in response_data}

        assert titles == {"Test Title 1", "Test Title 2"}

    @pytest.mark.anyio
    async def test_get_all_tasks_without_jwt(self, client):
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

        user_data = response.json()

        login_data = {
            "username": user_data["username"],
            "password": "testpassword123"
        }

        response = await client.post("/auth/login", data=login_data)
        
        assert response.status_code == 200
        response_data = response.json()

        access_token = response_data["access_token"]
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        task_1_data = {
            "title": "Test Title 1",
        }

        task_2_data = {
            "title": "Test Title 2",
        }

        response = await client.post("/tasks", 
                                     json=task_1_data,
                                     headers=headers)

        assert response.status_code == 201

        response = await client.post("/tasks", 
                                     json=task_2_data,
                                     headers=headers)

        assert response.status_code == 201


        response = await client.get("/tasks")

        assert response.status_code == 401

    @pytest.mark.anyio
    async def test_get_all_tasks_only_returns_current_user_tasks(self, client):
        # --------- User 1 --------
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

        user_data = response.json()

        login_data = {
            "username": user_data["username"],
            "password": "testpassword123"
        }

        response = await client.post("/auth/login", data=login_data)
        
        assert response.status_code == 200
        response_data = response.json()
        user_1_access_token = response_data["access_token"]

        task_data = {
            "title": "Test Title"
        }
        headers = {
            "Authorization": f"Bearer {user_1_access_token}"
        }
        response = await client.post("/tasks", json=task_data, headers=headers)
        assert response.status_code == 201
        created_task_data = response.json()

        # --------- User 2 --------
        data_2 = {
            "username": "testuser_2",
            "password": "testpassword123",
            "email": "test2@example.com"
        }

        response = await client.post(
            "/users",
            json=data_2
        ) 

        assert response.status_code == 201

        user_2_data = response.json()

        login_2_data = {
            "username": user_2_data["username"],
            "password": "testpassword123"
        }

        response = await client.post("/auth/login", data=login_2_data)
        
        assert response.status_code == 200
        response_2_data = response.json()
        user_2_access_token = response_2_data["access_token"]

        task_2_data = {
            "title": "Test Title 2"
        }

        headers_2 = {
            "Authorization": f"Bearer {user_2_access_token}"
        }
        response = await client.post("/tasks", json=task_2_data, headers=headers_2)
        assert response.status_code == 201
        created_task_data_2 = response.json()

        # -------- Retrieval User 2 --------
        response = await client.get("/tasks", headers=headers)

        assert response.status_code == 200
        retrieved_task_1_data = response.json()

        task_1_titles = {task["title"] for task in retrieved_task_1_data}
        
        assert task_1_titles == {"Test Title"}

        # ------ Retrieval User 2 ----------
        response = await client.get("/tasks", headers=headers_2)

        assert response.status_code == 200
        retrieved_task_2_data = response.json()

        task_2_titles = {task["title"] for task in retrieved_task_2_data}

        assert task_2_titles == {"Test Title 2"}


    @pytest.mark.anyio
    async def test_get_all_tasks_with_no_tasks(self, client):
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

        user_data = response.json()

        login_data = {
            "username": user_data["username"],
            "password": "testpassword123"
        }

        response = await client.post("/auth/login", data=login_data)
        
        assert response.status_code == 200
        response_data = response.json()
        access_token = response_data["access_token"]

        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        response = await client.get("/tasks", headers=headers)

        assert response.status_code == 200

        retrieved_tasks = response.json()

        assert len(retrieved_tasks) == 0