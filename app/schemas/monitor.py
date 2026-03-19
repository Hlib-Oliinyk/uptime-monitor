from datetime import datetime

from pydantic import BaseModel, ConfigDict, HttpUrl, Field


class MonitorCreate(BaseModel):
    url: HttpUrl
    interval: int = Field(ge=30)
    is_active: bool


class MonitorUpdate(BaseModel):
    url: HttpUrl | None = None
    interval: int | None = None
    is_active: bool | None = None


class MonitorResponse(BaseModel):
    id: int
    url: HttpUrl
    interval: int
    is_active: bool
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)