from fastapi.responses import JSONResponse
from app.exceptions.user import UserExists, UserNotFound


def setup_exception_handler(app):
    @app.exception_handler(UserNotFound)
    async def user_not_found_handler(request, exc):
        return JSONResponse(
            status_code=404,
            content={"details":"User not found"}
        )

    @app.exception_handler(UserExists)
    async def user_exists_handler(request, exc):
        return JSONResponse(
            status_code=400,
            content={"details":"User already exists"}
        )