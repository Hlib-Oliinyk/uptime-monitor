from app.repositories.user import UserRepository
from app.schemas.user import UserCreate
from app.models.user import User


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def create_user(self, data: UserCreate) -> User:
        exists = self.repo.user_exists(data.email, data.username)
        if exists:
            raise # Add raise

        user_dict = data.model_dump()
        return await self.repo.create(**user_dict)

    async def get_user(self, user_id: int) -> User:
        user = await self.repo.get_by_id(user_id)
        if user is None:
            raise # Add raise
        return user