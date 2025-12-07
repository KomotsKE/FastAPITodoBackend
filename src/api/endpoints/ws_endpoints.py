from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import logging

from src.websocket.connection_manager import manager

logger = logging.getLogger("websocket")
router = APIRouter()


@router.websocket("/ws/tasks")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket-эндпоинт для получения событий задач в реальном времени."""
    await manager.connect(websocket)
    try:
        while True:
            # Слушаем входящие сообщения (могут быть ping/keepalive от клиента)
            data = await websocket.receive_text()
            logger.debug(f"Received from websocket: {data}")
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
    except Exception as e:
        logger.warning(f"WebSocket error: {e}")
        await manager.disconnect(websocket)
