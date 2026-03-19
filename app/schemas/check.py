from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CheckResponse(BaseModel):
    id: int
    monitor_id: int
    status_code: int
    response_time: float
    checked_at: datetime

    model_config = ConfigDict(from_attributes=True)