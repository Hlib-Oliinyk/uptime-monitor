from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MonitorCreate(BaseModel):
    url: str
    interval: int
    is_active: bool
    user_id: int
    created_at: datetime


class MonitorResponse(BaseModel):
    id: int
    url: str
    interval: int
    is_active: bool
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)