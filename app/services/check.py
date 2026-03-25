from typing import Sequence

from app.models.check import Check
from app.repositories.check import CheckRepository
from app.repositories.monitor import MonitorRepository
from app.exceptions.monitor import MonitorNotFound


class CheckService:
    def __init__(self, repo: CheckRepository, monitor_repo: MonitorRepository):
        self.repo = repo
        self.monitor_repo = monitor_repo

    async def get_all_checks(self, monitor_id: int, user_id: int) -> Sequence[Check]:
        monitor = await self.monitor_repo.get_by_id(monitor_id)
        if monitor is None or monitor.user_id != user_id:
            raise MonitorNotFound()

        checks = await self.repo.get_all_by_monitor_id(monitor_id)
        return checks