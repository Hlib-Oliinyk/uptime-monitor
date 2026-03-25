from typing import Annotated

from fastapi import APIRouter, Depends

from app.services.check import CheckService
from app.dependencies import get_check_service, get_current_user
from app.schemas.monitor import MonitorResponse
from app.models.user import User


router = APIRouter(
    prefix="/check",
    tags=["Check"]
)


@router.get("/{monitor_id}", response_model=list[MonitorResponse])
async def get_all_checks(
    monitor_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[CheckService, Depends(get_check_service)]
):
    return await service.get_all_checks(monitor_id, current_user.id)


