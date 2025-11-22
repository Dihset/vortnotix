import logging

from fastapi import FastAPI

from src.api.router import router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def webserver_factory() -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    return app
