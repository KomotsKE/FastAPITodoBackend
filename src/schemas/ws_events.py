from enum import Enum
from datetime import datetime
from pydantic import BaseModel
from src.schemas.task import TaskOut


class TaskEventType(str, Enum):
    """Типы событий для задач"""
    TASK_CREATED = "task_created"
    TASK_UPDATED = "task_updated"
    TASK_DELETED = "task_deleted"
    BACKGROUND_TASK_RUN = "background_task_run"


class TaskEvent(BaseModel):
    """WebSocket-событие о изменении задачи"""
    event_type: TaskEventType
    task: TaskOut
    timestamp: datetime

    class Config:
        use_enum_values = False  # сохраняем Enum, но при JSON будет "task_created"
