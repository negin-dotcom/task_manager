from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User
from app.schemas.user import UserCreate, UserUpdate

from app.core.security import hash_password


async def create_user(
    data: UserCreate,
    db: AsyncSession
) -> User:
    
    user = User(
        username=data.username, 
        password=hash_password(data.password),
        email=data.email
    )

    db.add(user)

    try:
        await db.commit()
        await db.refresh(user)

    except IntegrityError:
        await db.rollback()
        raise

    return user


async def get_user_by_username(
    username: str,
    db: AsyncSession
) -> User | None:
    
    result = await db.execute(
        select(User)
        .where(User.username == username)
    )

    return result.scalar_one_or_none()


async def get_user_by_id(
    user_id: int,
    db: AsyncSession
) -> User | None:
    
    result = await db.execute(
        select(User)
        .where(User.id == user_id)
    )

    return result.scalar_one_or_none()


async def update_user(
    user_id: int,
    data: UserUpdate,
    db: AsyncSession
) -> User:

    user = await get_user_by_id(user_id, db)

    if user is None:
        raise ValueError("User not found.")

    updated_data = data.model_dump(exclude_unset=True)

    for field, value in updated_data.items():
        setattr(user, field, value)

    await db.commit()
    await db.refresh(user)

    return user


async def delete_user(
    user_id: int,
    db: AsyncSession
) -> None:

    user = await get_user_by_id(user_id, db)

    if user is None:
        raise ValueError("User not found.")

    await db.delete(user)
    await db.commit()