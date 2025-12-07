from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import logging

from src.websocket.connection_manager import manager


router = APIRouter()


@router.websocket("/ws/tasks")
async def websocket_endpoint(websocket: WebSocket):
    """Получение событий задач в реальном времени"""
    await manager.connect(websocket)
    try:
        while True:
            # Слушаем входящие сообщения (могут быть ping/keepalive от клиента)
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
    except Exception as e:
        await manager.disconnect(websocket)
