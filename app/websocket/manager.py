from __future__ import annotations

import asyncio
from typing import List

from fastapi import WebSocket

from app.schemas.security import EventIngestResponse


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: List[WebSocket] = []
        self._lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        async with self._lock:
            self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket) -> None:
        async with self._lock:
            if websocket in self.active_connections:
                self.active_connections.remove(websocket)

    async def _broadcast(self, payload: dict) -> None:
        async with self._lock:
            connections = list(self.active_connections)
        for connection in connections:
            await connection.send_json(payload)

    def broadcast_event(self, event: EventIngestResponse) -> None:
        if not self.active_connections:
            return
        payload = {
            "event": event.event.id,
            "status": event.event.status.value,
            "confidence": event.event.confidence,
            "action": event.action,
            "alert": event.alert.id if event.alert else None,
        }
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(self._broadcast(payload))
        except RuntimeError:
            asyncio.run(self._broadcast(payload))


manager = ConnectionManager()
