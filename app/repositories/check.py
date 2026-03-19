from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.check import Check


class CheckRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_by_monitor_id(self, monitor_id: int) -> Sequence[Check]:
        stmt = select(Check).where(Check.monitor_id == monitor_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def create(self, **data) -> Check:
        check = Check(**data)
        self.db.add(check)
        await self.db.commit()
        await self.db.refresh(check)
        return check