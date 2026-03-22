from fastapi import FastAPI

from app.exceptions_handler import setup_exception_handler
from app.api.endpoints import router


app = FastAPI(
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