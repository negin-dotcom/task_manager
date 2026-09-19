from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TaskCreate(BaseModel):
    title: str 
    description: str | None = None


class TaskResponse(BaseModel):
    id: int 
    title: str
    completed: bool 
    created_at: datetime
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None