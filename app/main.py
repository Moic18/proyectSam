from __future__ import annotations

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database.session import engine
from app.models.security import Base
from app.routers import auth, events, faces, notifications
from app.services.face_recognition import face_service
from app.websocket.manager import manager

settings = get_settings()

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def load_model() -> None:
    face_service.load()


app.include_router(auth.router)
app.include_router(events.router)
app.include_router(faces.router)
app.include_router(notifications.router)


@app.websocket("/ws/events")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await manager.disconnect(websocket)