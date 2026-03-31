from typing import Sequence, Annotated
from datetime import datetime

from fastapi import Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.check import Check
from app.schemas.check import CheckPagination


class CheckRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_by_monitor_id_with_pagination(
        self,
        monitor_id: int,
        pagination: Annotated[CheckPagination, Depends(CheckPagination)]
    ) -> Sequence[Check]:
        stmt = (select(Check).where(Check.monitor_id == monitor_id)
                .limit(pagination.limit)
                .offset(pagination.offset))

        result = await self.db.execute(stmt)
        return result.scalars().all()

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

    async def successful_checks(self, monitor_id: int) -> int:
        stmt = select(func.count(Check.id)).where(Check.monitor_id == monitor_id, Check.status_code < 400)
        result = await self.db.execute(stmt)
        return result.scalar()

    async def total_checks(self, monitor_id: int) -> int:
        checks = await self.get_all_by_monitor_id(monitor_id)
        return len(checks)

    async def avg_response_time(self, monitor_id: int) -> float:
        stmt = select(func.avg(Check.response_time)).where(Check.monitor_id == monitor_id)
        result = await self.db.execute(stmt)
        return round(result.scalar(), 3)

    async def last_check(self, monitor_id: int) -> datetime:
        stmt = select(func.max(Check.checked_at)).where(Check.monitor_id == monitor_id)
        result = await self.db.execute(stmt)
        return result.scalar()