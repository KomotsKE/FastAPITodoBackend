import logging
from typing import Set
from fastapi import WebSocket
from src.schemas.ws_events import TaskEvent

logger = logging.getLogger("websocket")

class ConnectionManager:
    """Управляет активными WebSocket-соединениями и отправляет broadcast-события."""

    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        """Принять новое соединение и добавить в активные."""
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info(f"Connected: {id(websocket)} | Active: {len(self.active_connections)}")

    async def disconnect(self, websocket: WebSocket):
        """Удалить соединение из активных и закрыть его."""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"Disconnected: {id(websocket)} | Active: {len(self.active_connections)}")

            try:
                await websocket.close()
            except Exception as e:
                logger.warning(f"Close error ({id(websocket)}): {e}")

    async def broadcast(self, event: TaskEvent):
        """Отправить событие всем подписанным клиентам."""
        if not self.active_connections:
            return

        message = event.model_dump_json()
        disconnected = []

        for websocket in list(self.active_connections):
            try:
                await websocket.send_text(message)
            except Exception as e:
                logger.warning(f"Send error ({id(websocket)}): {e}")
                disconnected.append(websocket)

        for ws in disconnected:
            await self.disconnect(ws)

        logger.info(f"Broadcast delivered to {len(self.active_connections)} clients")


manager = ConnectionManager()