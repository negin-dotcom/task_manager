import pytest 
from httpx import ASGITransport, AsyncClient
from app.main import app

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)

from app.core.config import settings
from app.db.base import Base
from app.db.session import get_db


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, 
                           base_url="http://test") as client:
        yield client


test_engine = create_async_engine(
    settings.test_database_url
)

TestSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


@pytest.fixture(autouse=True)
async def setup_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield 

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await test_engine.dispose()


async def override_get_db():
    async with TestSessionLocal() as db:
        yield db


app.dependency_overrides[get_db] = override_get_db