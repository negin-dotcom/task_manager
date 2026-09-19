from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)

from app.core.config import settings


engine = create_async_engine(
    settings.database_url
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_db():
    db = AsyncSessionLocal()

    try:
        yield db

    except Exception:
        await db.rollback()
        raise 

    finally:
        await db.close()