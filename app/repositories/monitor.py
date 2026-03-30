from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.monitor import Monitor
from app.schemas.monitor import MonitorUpdate


class MonitorRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, monitor_id: int) -> Monitor | None:
        stmt = select(Monitor).where(Monitor.id == monitor_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all_by_user_id(self, user_id: int) -> Sequence[Monitor]:
        stmt = select(Monitor).where(Monitor.user_id == user_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def create(self, **data) -> Monitor:
        monitor = Monitor(**data)
        self.db.add(monitor)
        await self.db.commit()
        await self.db.refresh(monitor)
        return monitor

    async def update(self, monitor: Monitor, monitor_update: MonitorUpdate) -> Monitor:
        if monitor_update.url is not None:
            monitor.url = str(monitor_update.url)
        if monitor_update.interval is not None:
            monitor.interval = monitor_update.interval
        if monitor_update.is_active is not None:
            monitor.is_active = monitor_update.is_active

        await self.db.commit()
        await self.db.refresh(monitor)
        return monitor

    async def delete(self, monitor: Monitor) -> bool:
        await self.db.delete(monitor)
        await self.db.commit()
        return True

    async def get_active_monitors(self) -> Sequence[Monitor]:
        stmt = select(Monitor).where(Monitor.is_active == True)
        result = await self.db.execute(stmt)
        return result.scalars().all()