from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

from datetime import datetime


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(nullable=False)

    description: Mapped[str | None] = mapped_column(nullable=True,
                                                    default="")

    completed: Mapped[bool] = mapped_column(nullable=False,
                                            default=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"),
                                         nullable=False)

    user: Mapped["User"] = relationship("User",
                                        back_populates="tasks")
    