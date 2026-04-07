import logging

from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.endpoints import router
from app.utils.logger import HTTPLoggerMiddleware
from app.exceptions_handler import setup_exception_handler
from app.tasks.restart_active_monitors import restart_active_monitors_task


@asynccontextmanager
async def lifespan(app: FastAPI):
    restart_active_monitors_task.delay()
    yield


app = FastAPI(
    lifespan=lifespan,
    docs_url="/api/docs"
)

logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

app.include_router(router)
setup_exception_handler(app)
app.add_middleware(HTTPLoggerMiddleware)


@app.get("/")
def root():
    return {
        "project": "uptime-monitor",
        "docs": "/api/docs"
    }