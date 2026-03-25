from pydantic import EmailStr

from app.repositories.user import UserRepository
from app.schemas.user import UserCreate
from app.models.user import User
from app.exceptions.user import UserExists, UserNotFound
from app.securities.hashing import hash_password, verify_password
from app.exceptions.token import InvalidCredentials


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def create_user(self, data: UserCreate) -> User:
        exists = await self.repo.user_exists(data.email, data.username)
        if exists:
            raise UserExists()

        user_dict = data.model_dump()
        user_dict["password"] = hash_password(user_dict.pop("password"))

        return await self.repo.create(**user_dict)

    async def get_user(self, user_id: int) -> User:
        user = await self.repo.get_by_id(user_id)
        if user is None:
            raise UserNotFound()
        return user

    async def authenticate_user(
        self,
        user_email: EmailStr,
        password: str
    ) -> User:
        user = await self.repo.get_by_email(user_email)
        if user is None or not verify_password(password, user.password):
            raise InvalidCredentials()
        return user
