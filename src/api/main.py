from fastapi import FastAPI
from src.api.endpoints import tasks_endpoints, ws_endpoints

app = FastAPI()

# Включить роутеры
app.include_router(tasks_endpoints.router)
app.include_router(ws_endpoints.router)

