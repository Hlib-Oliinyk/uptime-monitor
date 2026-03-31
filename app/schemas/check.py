from datetime import datetime

from pydantic import Field
from pydantic import BaseModel, ConfigDict


class CheckResponse(BaseModel):
    id: int
    monitor_id: int
    status_code: int
    response_time: float
    checked_at: datetime

    model_config = ConfigDict(from_attributes=True)
    

class CheckPagination(BaseModel):
    limit: int = Field(5, ge=0, le=100)
    offset: int = Field(0, ge=0)