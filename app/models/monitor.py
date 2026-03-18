import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Monitor(Base):
    __tablename__ = "monitors"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    url: Mapped[str] = mapped_column(nullable=False)
    interval: Mapped[int] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="monitors")



