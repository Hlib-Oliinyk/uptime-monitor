from typing import Sequence, Annotated
from fastapi import Depends

from app.models.check import Check
from app.schemas.check import CheckPagination
from app.utils.exceptions.check import CheckNotFound
from app.utils.exceptions.monitor import MonitorNotFound
from app.repositories.check import CheckRepository
from app.repositories.monitor import MonitorRepository


class CheckService:
    def __init__(self, repo: CheckRepository, monitor_repo: MonitorRepository):
        self.repo = repo
        self.monitor_repo = monitor_repo

    @staticmethod
    def calculate_percentage(total: int, successful: int) -> float:
        if total == 0:
            return  0.0

        percentage = (successful * 100) / total
        return round(percentage, 2)

    async def get_all_checks(
        self,
        monitor_id: int,
        user_id: int,
        pagination: Annotated[CheckPagination, Depends(CheckPagination)]
    ) -> Sequence[Check]:
        monitor = await self.monitor_repo.get_by_id(monitor_id)
        if monitor is None or monitor.user_id != user_id:
            raise MonitorNotFound()

        checks = await self.repo.get_all_by_monitor_id_with_pagination(monitor_id, pagination)
        return checks

    async def uptime_percentage(self, monitor_id: int, total_checks: int) -> float:
        successful_checks = await self.repo.successful_checks(monitor_id)
        percentage = CheckService.calculate_percentage(total_checks, successful_checks)
        return percentage

    async def get_monitor_stats(self, monitor_id: int, user_id: int):
        monitor = await self.monitor_repo.get_by_id(monitor_id)
        if monitor is None or monitor.user_id != user_id:
            raise MonitorNotFound()

        total_checks = await self.repo.total_checks(monitor_id)

        if total_checks == 0:
            raise CheckNotFound()

        stats = {
            "uptime_percentage": await self.uptime_percentage(monitor_id, total_checks),
            "avg_response_time": await self.repo.avg_response_time(monitor_id),
            "total_checks": total_checks,
            "last_check": await self.repo.last_check(monitor_id)
        }
        return stats