from sqlalchemy import select, or_, exists
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr

from app.models.user import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_email(self, user_email: EmailStr) -> User | None:
        stmt = select(User).where(User.email == user_email)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def user_exists(self, user_email: EmailStr, user_username: str) -> bool:
        stmt = select(
            exists().where(
                or_(User.email == user_email, User.username == user_username)
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar()

    async def create(self, **data) -> User:
        user = User(**data)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user


