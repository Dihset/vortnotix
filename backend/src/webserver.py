from fastapi import FastAPI

from src.api.router import router


def webserver_factory() -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    return app
