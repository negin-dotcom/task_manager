from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select

from app.core.security import decode_access_token
from app.db.models.user import User
from app.db.session import get_db

from sqlalchemy.ext.asyncio import AsyncSession


oauth2_schema = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


async def get_current_user(
    token: str = Depends(oauth2_schema),
    db: AsyncSession = Depends(get_db)
) -> User:

    try:
        payload = decode_access_token(token=token)
        print("payload", payload)

    except ValueError as e:
        print("error as ", e)
        raise HTTPException(
            detail="Invalid or expired token.",
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            detail="Invalid authentication credentials.",
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    try:
        user_id = int(user_id)

    except (TypeError, ValueError):
        raise HTTPException(
            detail="Invalid authentication credentials.",
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    result = await db.execute(
        select(User)
        .where(User.id == user_id)
    )

    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            detail="User not found.",
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    return user