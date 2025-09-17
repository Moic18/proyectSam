from __future__ import annotations

from typing import Annotated, List

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database.session import get_session
from app.models.security import AccessEvent, Device
from app.schemas.security import EventIngestResponse
from app.services.event_service import process_event

router = APIRouter(prefix="/events", tags=["events"])


@router.post("/ingest", response_model=EventIngestResponse)
async def ingest_event(
    device_token: Annotated[str, Form(...)],
    image: UploadFile = File(...),
    session: Session = Depends(get_session),
) -> EventIngestResponse:
    image_bytes = await image.read()
    try:
        response = process_event(
            session,
            device_token=device_token,
            image_bytes=image_bytes,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return response


@router.get("/recent", response_model=List[dict])
def recent_events(session: Session = Depends(get_session)) -> List[dict]:
    events = session.query(AccessEvent).order_by(AccessEvent.timestamp.desc()).limit(20).all()
    return [
        {
            "id": event.id,
            "timestamp": event.timestamp,
            "status": event.status.value,
            "confidence": event.confidence,
            "user": event.user.name if event.user else None,
            "device": event.device.name if event.device else None,
            "snapshot_path": event.snapshot_path,
        }
        for event in events
    ]


@router.post("/register-device", response_model=dict)
def register_device(name: Annotated[str, Form(...)], token: Annotated[str, Form(...)], session: Session = Depends(get_session)) -> dict:
    existing = session.query(Device).filter(Device.token == token).first()
    if existing:
        raise HTTPException(status_code=400, detail="Device token already exists")
    device = Device(name=name, token=token)
    session.add(device)
    session.commit()
    session.refresh(device)
    return {"id": device.id, "name": device.name, "token": device.token}