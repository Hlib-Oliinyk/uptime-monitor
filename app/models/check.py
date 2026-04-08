import datetime

from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Check(Base):
    __tablename__ = "checks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    monitor_id: Mapped[int] = mapped_column(ForeignKey("monitors.id"), index=True)
    status_code: Mapped[int] = mapped_column(nullable=False)
    response_time: Mapped[float] = mapped_column(nullable=False)
    checked_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())

    monitor: Mapped["Monitor"] = relationship(back_populates="checks")