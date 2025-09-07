from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .database import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("username", name="uq_users_username"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(100), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    tasks: Mapped[list["Task"]] = relationship("Task", back_populaters="ower", cascade="all, delete-orphan")


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=False)
    is_done: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    ower_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    ower: Mapped[User] = relationship("User", back_populaters="tasks")