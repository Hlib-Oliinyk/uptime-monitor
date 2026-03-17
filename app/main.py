from fastapi import FastAPI


app = FastAPI(
    docs_url="/api/docs"
)

@app.get("/")
def root():
    return {
        "project": "uptime-monitor",
        "docs": "/api/docs"
    }