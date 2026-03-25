from fastapi import Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import AsyncSessionLocal
from app.exceptions.token import InvalidCredentials
from app.models.user import User
from app.repositories.user import UserRepository
from app.repositories.token import TokenRepository
from app.repositories.monitor import MonitorRepository
from app.services.user import UserService
from app.services.token import TokenService
from app.services.monitor import MonitorService
from app.securities.authorization.jwt import jwt_generator


async def get_db():
    async with AsyncSessionLocal() as db:
        yield db


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(UserRepository(db))


def get_token_service(db: AsyncSession = Depends(get_db)) -> TokenService:
    return TokenService(TokenRepository(db), UserRepository(db))


def get_monitor_service(db: AsyncSession = Depends(get_db)) -> MonitorService:
    return MonitorService(MonitorRepository(db))


def get_token_from_header_or_cookie(request: Request) -> str:
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer: "):
        return auth_header[7:]

    cookie_token = request.cookies.get("access_token")
    if cookie_token:
        return cookie_token

    raise InvalidCredentials()


async def get_current_user(
    token: str = Depends(get_token_from_header_or_cookie),
    user_service: UserService = Depends(get_user_service)
) -> User:
    user_id = jwt_generator.get_details_from_token(token)
    user = await user_service.get_user(user_id)
    return user
