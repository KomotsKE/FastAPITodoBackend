import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.api.endpoints import tasks_endpoints, ws_endpoints, background_task_endpoints


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(background_task_endpoints.periodic_task())
    try:
        yield
    finally:
        task.cancel()


app = FastAPI(lifespan=lifespan)


app.include_router(tasks_endpoints.router)
app.include_router(ws_endpoints.router)
app.include_router(background_task_endpoints.router)