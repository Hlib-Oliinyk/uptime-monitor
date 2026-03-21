from typing import Sequence

from app.models.check import Check
from app.repositories.check import CheckRepository


class CheckService:
    def __init__(self, repo: CheckRepository):
        self.repo = repo

    async def get_all_checks(self, monitor_id: int) -> Sequence[Check]:
        checks = await self.repo.get_all_by_monitor_id(monitor_id)
        return checks