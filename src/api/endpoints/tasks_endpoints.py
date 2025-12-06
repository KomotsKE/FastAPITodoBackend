from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from database.session import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.models.task import Task
from schemas.task import TaskCreate, TaskOut, TaskUpdate

router = APIRouter()


@router.get("/tasks", response_model=list[TaskOut])
async def get_tasks(session: AsyncSession =Depends(get_async_session)):
    tasks = await session.execute(select(Task))
    return tasks.scalars().all()



@router.get("/tasks/{task_id}", response_model=TaskOut)
async def get_task(task_id: UUID, session: AsyncSession =Depends(get_async_session)):
    """получить задачу"""
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(404, "task not found")
    return task

@router.post("/tasks", response_model=TaskOut)
async def create_task(task_payload: TaskCreate, session: AsyncSession =Depends(get_async_session)):
    """создать задачу"""
    task = Task(
        title=task_payload.title,
        description=task_payload.description,
        completed=False,
    )

    session.add(task)
    await session.commit()
    await session.refresh(task)

    return task

@router.patch("/tasks/{task_id}", response_model=TaskOut)
async def update_task(task_id: UUID, task_payload: TaskUpdate, session: AsyncSession =Depends(get_async_session)):
    """обновление задачи"""
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(404, "task not found")
    
    changed = False

    if task_payload.title is not None:
        task.title = task_payload.title
        changed = True

    if task_payload.description is not None:
        task.description = task_payload.description
        changed = True

    if task_payload.completed is not None:
        task.completed = task_payload.completed
        changed = True
    
    if changed:
        session.add(task)
        await session.commit()
        await session.refresh(task)

    return task


@router.delete("/tasks/{task_id}")
async def delete_task(task_id: UUID, session: AsyncSession =Depends(get_async_session)):
    """удалить задачу"""
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(404, "task not found")
    
    await session.delete(task)
    await session.commit()
    
    return {"status": "ok"}



@router.post("/task-generator/run")
async def run_task_generator():
    """принудительный запуск фоновой задачи"""
    pass

