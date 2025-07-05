from fastapi import FastAPI


def webserver_factory() -> FastAPI:
    app = FastAPI()
    return app
