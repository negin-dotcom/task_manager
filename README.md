# Async Task Manager

## A RESTful task management API built with FastAPI, async SQLAlchemy, and PostgreSQL.

### This project provides user authentication, JWT-based authorization, and task management with user-specific task ownership.


## Features 
- User registration and authentication
- Environment-based configuration
- Database migrations with Alembic 
- PostgreSQL database
- Asynchronous database operations 
- CRUD operations for tasks
- Secure password hashing with Argon2
- Documentation with FastAPI


## Tech Stack
- Python 3.12
- FastAPI - REST API framework
- SQLAlchemy - ORM and database interaction
- asyncpg - PostgreSQL async driver
- PostgreSQL - relational database
- Pydantic - data validation and schemas
- Alembic - database migrations
- python-jose - JWT handling
- Argon2 - password hashing
- pytest - testing
- HTTPX - asynchronous API testing
- uv - Python package and environment management



## Project Structure
```text
src/app/
├── alembic/
│   └── versions/
├── core/
│   └── config.py
├── db/
│   ├── models/
│   ├── base.py
│   └── session.py
├── routers/
│   ├── auth.py
│   ├── task.py
│   └── user.py
├── schemas/
│   ├── task.py
│   └── user.py
├── services/
│   ├── task.py
│   └── user.py
├── tests/
├── .env.example
├── alembic.ini
└── main.py
```

## Directory Overview
- core/ - application configuration
- db/ - database models
- routers/ - API endpoints
- schemas/ - request and response schemas 
- services/ - application logic
- tests/ - automated tests
- alembic/ - database migration files


## Installation
### Prerequisites
#### Make sure you have the following installed:
- Python 3.12+
- PostgreSQL 
- uv

### Clone the repository
```bash
git clone https://github.com/negin-dotcom/task_manager.git

cd task_manager
```

### Install Dependencies 
```bash 
uv sync
```


## Environment Configuration
### Create a `.env` file inside `src/app/`:
```bash
src/app/.env 
```

### Use `src/app/.env.example` as a template:
```bash
cp src/app/.env.example src/app/.env
```
### Then update values in `.env` with your PostgreSQL credentials and a secure JWT secret.

### The `.env` file contains sensitive configuration and must not be committed to Git.


## Database Setup
### Create the PostgreSQL databases specified in `DATABASE_URL` AND `TEST_DATABASE_URL` in your `.env` file.



## Running the Application
### From the project root, run:
```bash
uv run uvicorn app.main:app --app-dir src
```
### The API will be available at:
```bash
http://127.0.0.1:8000
```


## API Documentation
### FastAPI provides interactive API documentation automatically.

## Swagger UI
```markdown
http://127.0.0.1:8000/docs
```

## ReDoc
```markdown
http://127.0.0.1:8000/redoc
```

## Authentication
### The API uses `JWT bearer tokens` for authentication.

### The authentication flow is:
1. Register a user through `POST /users`.
2. Log in through `POST /auth/login`.
3. Receive an access token.
4. Include the token when accessing protected endpoints.

### Protected endpoints use the following header:
```bash
Authorization: Bearer <access_token>
```

## API endpoints

### Users

| Method | Endpoint    | Description          | Auth |
| ------ | ----------- | -------------------- | ---- |
| `POST` | `/users`    | Register a new user  | No   |
| `GET`  | `/users/me` | Get the current user | Yes  |

### Authentication

| Method | Endpoint      | Description                       | Auth |
| ------ | ------------- | --------------------------------- | ---- |
| `POST` | `/auth/login` | Log in and obtain an access token | No   |

### Tasks

| Method   | Endpoint           | Description                  | Auth |
| -------- | ------------------ | ---------------------------- | ---- |
| `POST`   | `/tasks`           | Create a task                | Yes  |
| `GET`    | `/tasks`           | Get the current user's tasks | Yes  |
| `GET`    | `/tasks/{task_id}` | Get a task                   | Yes  |
| `PATCH`  | `/tasks/{task_id}` | Update a task                | Yes  |
| `DELETE` | `/tasks/{task_id}` | Delete a task                | Yes  |


## Testing
### The project includes asynchronous API tests using `pytest` and `HTTPX`.

### The test suite covers:
- User registration and validation
- Authentication and login
- JWT validation 
- Nonexistent resources
- Invalid request data 
- Task CRUD
- Task ownership and user isolation
- Authentication requirements

### Run the test suite with:
```bash
uv run pytest
```


## Database Migrations
### The project uses `Alembic` to manage database schema changes.

### Apply existing migrations:
```bash
uv run alembic -c src/app/alembic.ini upgrade head
```

### Check the current migration:
```bash
uv run alembic -c src/app/alembic.ini current
```

### Check the database synchronization with SQLAlchemy models:
```bash
uv run alembic -c src/app/alembic.ini check
```

### To create a new migration after changing the models:
```bash
uv run alembic -c src/app/alembic.ini revision --autogenerate -m "describe the change"
```