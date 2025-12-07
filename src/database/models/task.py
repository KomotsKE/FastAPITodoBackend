from datetime import datetime
import uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, Boolean, Text, DateTime, func

from .base import Base


class Task(Base):
    """Модель задачи"""
    __tablename__ = "tasks"
    """Уникальный идентификатор задачи"""
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid.uuid4
    )
    """Заголовок задачи"""
    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )
    """Описание задачи"""
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
    """Статус выполнения задачи"""
    completed: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False
    )
    """Дата и время создания задачи"""
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
