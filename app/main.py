from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.endpoints import router
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


setup_exception_handler(app)
app.include_router(router)

@app.get("/")
def root():
    return {
        "project": "uptime-monitor",
        "docs": "/api/docs"
    }