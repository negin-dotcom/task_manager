from fastapi import FastAPI

from app.routers.user import router as user_router
from app.routers.task import router as task_router


def create_app():
    app = FastAPI(
        title="Async Task Manager",
        version="0.1.0"
    )

    app.include_router(user_router)
    app.include_router(task_router)


    @app.get("/")
    async def root():
        return {"message": "hello from async fastapi"}

    return app 


app = create_app()