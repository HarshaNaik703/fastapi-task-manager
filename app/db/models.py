from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Enum
)
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
import datetime

from .session import Base


# -------------------- ENUMS --------------------

class UserRole(PyEnum):
    user = "user"
    admin = "admin"


class TaskStatus(PyEnum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"


class TaskPriority(PyEnum):
    low = "low"
    medium = "medium"
    high = "high"


# -------------------- USER MODEL --------------------

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)

    role = Column(
        Enum(UserRole),
        nullable=False,
        default=UserRole.user
    )

    is_active = Column(Boolean, default=True)

    created_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        nullable=False
    )

    tasks = relationship(
        "Task",
        back_populates="owner",
        cascade="all, delete-orphan"
    )


# -------------------- TASK MODEL --------------------

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)

    status = Column(
        Enum(TaskStatus),
        nullable=False,
        default=TaskStatus.pending
    )

    priority = Column(
        Enum(TaskPriority),
        nullable=False
    )

    due_date = Column(DateTime, nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        nullable=False
    )

    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False
    )

    owner_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )

    owner = relationship(
        "User",
        back_populates="tasks"
    )
