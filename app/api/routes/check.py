from typing import Annotated

from fastapi import APIRouter, Depends

from app.models.user import User
from app.schemas.check import CheckResponse, CheckPagination
from app.services.check import CheckService
from app.schemas.monitor import MonitorStats
from app.dependencies import get_check_service, get_current_user


router = APIRouter(
    prefix="/check",
    tags=["Check"]
)


@router.get("/{monitor_id}", response_model=list[CheckResponse])
async def get_all_checks(
    monitor_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[CheckService, Depends(get_check_service)],
    pagination: Annotated[CheckPagination, Depends(CheckPagination)]
):
    return await service.get_all_checks(monitor_id, current_user.id, pagination)


@router.get("/{monitor_id}/stats", response_model=MonitorStats)
async def get_monitor_stats(
    monitor_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[CheckService, Depends(get_check_service)]
):
    return await service.get_monitor_stats(monitor_id, current_user.id)