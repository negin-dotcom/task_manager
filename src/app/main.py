from fastapi import FastAPI


def create_app():
    app = FastAPI(
        title="Async Task Manager",
        version="0.1.0"
    )

    @app.get("/")
    def root():
        return {"message": "hello from async fastapi"}

    return app 


app = create_app()