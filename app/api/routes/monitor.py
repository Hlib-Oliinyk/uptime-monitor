from typing import Annotated

from fastapi import APIRouter, Depends

from app.services.monitor import MonitorService
from app.dependencies import get_monitor_service, get_current_user
from app.models.user import User
from app.schemas.monitor import MonitorResponse, MonitorCreate, MonitorUpdate
from app.tasks.check_monitor import check_monitor_task


router = APIRouter(
    prefix="/monitor",
    tags=["Monitor"],
)


@router.get("/", response_model=list[MonitorResponse])
async def get_all_monitors(
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[MonitorService, Depends(get_monitor_service)]
):
    return await service.get_all_monitor(current_user.id)


@router.get("/{monitor_id}", response_model=MonitorResponse)
async def get_monitor(
    monitor_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[MonitorService, Depends(get_monitor_service)]
):
    monitor = await service.get_monitor(monitor_id, current_user.id)
    return monitor


@router.post("/", response_model=MonitorResponse)
async def create_monitor(
    data: MonitorCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[MonitorService, Depends(get_monitor_service)],
):
    monitor = await service.create_monitor(current_user.id, data)
    check_monitor_task.delay(monitor.id)
    return monitor


@router.patch("/{monitor_id}", response_model=MonitorResponse)
async def update_monitor(
    monitor_id: int,
    data: MonitorUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[MonitorService, Depends(get_monitor_service)],
):
    monitor = await service.update_monitor(monitor_id, current_user.id, data)
    return monitor


@router.delete("/{monitor_id}")
async def delete_monitor(
    monitor_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[MonitorService, Depends(get_monitor_service)]
):
    return await service.delete_monitor(monitor_id, current_user.id)