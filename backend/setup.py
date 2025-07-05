import uvicorn

from src.webserver import webserver_factory

if __name__ == "__main__":
    uvicorn.run(webserver_factory(), host="0.0.0.0", port=8000)
