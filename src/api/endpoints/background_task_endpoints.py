import asyncio
from datetime import datetime, timezone
import random
import httpx
from fastapi import APIRouter, BackgroundTasks, Depends
from src.schemas.task import TaskOut
from src.schemas.ws_events import TaskEvent, TaskEventType
from src.database.session import get_async_session
from src.database.models.task import Task
from sqlalchemy.ext.asyncio import AsyncSession
from src.websocket.connection_manager import manager


router = APIRouter()
SLEEP_TIME = 60  # seconds


async def fetch_data() -> list[dict]:
    """Получение данных из внешнего API для генерации задач."""
    async with httpx.AsyncClient() as client:
        response = await client.get("https://jsonplaceholder.typicode.com/todos")
        response.raise_for_status()
        return response.json()
    
async def generate_tasks(session: AsyncSession):
    """Фоновая задача: добавление случайных 3 задач в базу."""
    data = await fetch_data()
    random_tasks = random.sample(data, k=min(3, len(data)))

    for item in random_tasks:
        task = Task(
            title=item["title"],
            description=f"Задача с внешнего API: {item['title']}",
            completed=item["completed"]
        )
        session.add(task)

    await session.commit()
    
    event = TaskEvent(
            event_type=TaskEventType.BACKGROUND_TASK_RUN,
            task=TaskOut.model_validate(task),
            timestamp=datetime.now(timezone.utc)
        )
    await manager.broadcast(event)

@router.post("/task-generator/run")
async def run_task_generator(
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_async_session)
):
    """Принудительный запуск фоновой генерации задач через BackgroundTasks."""
    background_tasks.add_task(generate_tasks, session)
    return {"status": "started"}


async def periodic_task():
    """Автоматический запуск фоновой генерации каждые 60 секунд."""
    while True:
        async for session in get_async_session():  
            await generate_tasks(session)
        await asyncio.sleep(SLEEP_TIME)

