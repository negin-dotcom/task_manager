from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.dependencies import get_current_user
from app.core.security import create_access_token, verify_password
from app.db.models.user import User
from app.db.session import get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate

from sqlalchemy.ext.asyncio import AsyncSession

from app.services import user as user_service

from sqlalchemy.exc import IntegrityError


router = APIRouter(
    tags=["User"]
)


@router.post("/auth/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    user = await user_service.get_user_by_username(
        username=form_data.username,
        db=db
    )

    if user is None:
        raise HTTPException(
            detail="Incorrect username or password.",
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    if not verify_password(
        form_data.password,
        user.password
    ):
        raise HTTPException(
            detail="Incorrect username or password.",
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    data = {"sub": str(user.id)}
    access_token = create_access_token(data=data)

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post("/users",
             response_model=UserResponse,
             status_code=status.HTTP_201_CREATED)
async def create_user(
    data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await user_service.create_user(
            data=data,
            db=db
        )
    except IntegrityError as e:
        error = str(e.orig)

        if "username" in error:
            raise HTTPException(
                detail="Username already exists.",
                status_code=status.HTTP_409_CONFLICT
            )

        if "email" in error:
            raise HTTPException(
                detail="Email already exists.",
                status_code=status.HTTP_409_CONFLICT
            )
            

        raise
            


@router.get("/users/me", 
            response_model=UserResponse)
async def get_me(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await user_service.get_user_by_id(
        user_id=current_user.id,
        db=db
    )


@router.patch("/users/me",
              response_model=UserResponse)
async def update_user(
    data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await user_service.update_user(
        user_id=current_user.id,
        data=data,
        db=db
    )


@router.delete("/users/me",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> None:

    await user_service.delete_user(
        user_id=current_user.id,
        db=db
    )
