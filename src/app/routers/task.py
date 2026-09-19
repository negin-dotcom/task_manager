from app.core.dependencies import get_current_user
from app.db.models.user import User
from app.db.session import get_db
from fastapi import Depends, APIRouter, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services import task as task_service


router = APIRouter(
    tags=["Task"]
)

@router.post("/tasks", 
             response_model=TaskResponse,
             status_code=status.HTTP_201_CREATED)
async def create_task(
    data: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await task_service.create_task(
        data=data,
        db=db,
        current_user=current_user
    )


@router.get("/tasks/{task_id}",
            response_model=TaskResponse)
async def get_task_by_id(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await task_service.get_task_by_id(
        task_id=task_id,
        db=db,
        current_user=current_user
    )


@router.get("/tasks", 
            response_model=list[TaskResponse])
async def get_tasks(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await task_service.get_tasks(
        db=db,
        current_user=current_user
    )


@router.patch("/tasks/{task_id}",
              response_model=TaskResponse)
async def update_task(
    task_id: int,
    data: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await task_service.update_task(
        task_id=task_id,
        data=data,
        db=db,
        current_user=current_user
    )


@router.delete("/tasks/{task_id}",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    await task_service.delete_task(
        task_id=task_id,
        db=db,
        current_user=current_user
    )