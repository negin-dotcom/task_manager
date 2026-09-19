from sqlalchemy import select

from app.db.models.task import Task
from app.db.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate

from sqlalchemy.ext.asyncio import AsyncSession


async def create_task(
    data: TaskCreate,
    db: AsyncSession,
    current_user: User
) -> Task:

    task = Task(
        title=data.title,
        description=data.description,
        user_id=current_user.id
    )

    try:
        db.add(task)
        await db.commit()
        await db.refresh(task)

        return task

    except Exception:
        await db.rollback()
        raise


async def get_task_by_id(
    task_id: int,
    db: AsyncSession,
    current_user: User
) -> Task | None:

    result = await db.execute(
        select(Task)
        .where(Task.id == task_id,
               Task.user_id == current_user.id)
    )

    return result.scalar_one_or_none()



async def get_tasks(
    db: AsyncSession,
    current_user: User
) -> list[Task]:

    result = await db.execute(
        select(Task)
        .where(Task.user_id == current_user.id)
    )

    return result.scalars().all()



async def update_task(
    task_id: int,
    data: TaskUpdate,
    db: AsyncSession,
    current_user: User
) -> Task | None:

    result = await db.execute(
        select(Task)
        .where(Task.id == task_id,
               Task.user_id == current_user.id)
    )

    task = result.scalar_one_or_none()

    if task is None:
        return None

    try:
        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(task, field, value)

        await db.commit()
        await db.refresh(task)

        return task 

    except Exception:
        await db.rollback()
        raise


async def delete_task(
    task_id: int,
    db: AsyncSession,
    current_user: User
) -> None:

    result = await db.execute(
        select(Task)
        .where(Task.id == task_id,
               Task.user_id == current_user.id)
    )

    task = result.scalar_one_or_none()

    if task is None:
        return 

    try:
        await db.delete(task)
        await db.commit()

    except Exception:
        await db.rollback()
        raise