from app.db.base import Base

from sqlalchemy.orm import mapped_column, Mapped, relationship


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(nullable=False,
                                          unique=True)

    password: Mapped[str] = mapped_column(nullable=False)

    email: Mapped[str] = mapped_column(nullable=False, 
                                       unique=True)

    tasks: Mapped[list["Task"]] = relationship("Task",
                                               back_populates="user",
                                               cascade="all, delete-orphan")
