from typing import Sequence

from app.repositories.monitor import MonitorRepository
from app.models.monitor import Monitor
from app.schemas.monitor import MonitorCreate, MonitorUpdate
from app.exceptions.monitor import MonitorNotFound
from app.tasks.check_monitor import check_monitor_task


class MonitorService:
    def __init__(self, repo: MonitorRepository):
        self.repo = repo

    async def create_monitor(self, user_id: int, data: MonitorCreate) -> Monitor:
        monitor_dict = data.model_dump(mode="json")
        monitor_dict["user_id"] = user_id
        monitor = await self.repo.create(**monitor_dict)

        check_monitor_task.delay(monitor.id)
        return monitor

    async def get_monitor(self, monitor_id: int, user_id: int) -> Monitor:
        monitor = await self.repo.get_by_id(monitor_id)
        if monitor is None or monitor.user_id != user_id:
            raise MonitorNotFound()
        return monitor

    async def get_all_monitor(self, user_id: int) -> Sequence[Monitor]:
        user_monitors = await self.repo.get_all_by_user_id(user_id)
        return user_monitors

    async def update_monitor(
        self,
        monitor_id: int,
        user_id: int,
        data: MonitorUpdate
    ) -> Monitor:
        monitor = await self.get_monitor(monitor_id, user_id)
        updated_monitor = await self.repo.update(monitor, data)

        if updated_monitor.is_active:
            check_monitor_task.delay(updated_monitor.id)

        return updated_monitor

    async def delete_monitor(self, monitor_id: int, user_id: int) -> bool:
        monitor = await self.get_monitor(monitor_id, user_id)
        return await self.repo.delete(monitor)