from __future__ import annotations

import secrets
from datetime import datetime
from pathlib import Path
from typing import Optional
from sqlalchemy.orm import Session

from app.config import get_settings
from app.models.security import AccessEvent, Alert, Device, EventStatus, User
from app.schemas.security import EventIngestResponse
from app.services.face_recognition import face_service
from app.websocket.manager import manager

settings = get_settings()


def _save_snapshot(image_bytes: bytes) -> Path:
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    filename = f"event_{timestamp}_{secrets.token_hex(4)}.jpg"
    path = settings.storage_dir / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(image_bytes)
    return path


def _maybe_create_alert(session: Session, event: AccessEvent) -> Optional[Alert]:
    if event.status == EventStatus.authorized:
        return None
    alert = Alert(event=event, message=event.message or "Intruder detected")
    session.add(alert)
    return alert


def process_event(
    session: Session,
    *,
    device_token: str,
    image_bytes: bytes,
) -> EventIngestResponse:
    device = session.query(Device).filter(Device.token == device_token, Device.is_active.is_(True)).first()
    if not device:
        raise ValueError("Unknown or inactive device")

    snapshot_path = _save_snapshot(image_bytes)

    predicted_user_id, confidence = face_service.predict(image_bytes)

    status = EventStatus.unknown
    message = "No model available"
    matched_user: Optional[User] = None

    if predicted_user_id is not None:
        matched_user = session.get(User, predicted_user_id)
        if matched_user:
            status = EventStatus.authorized if confidence >= settings.face_match_threshold else EventStatus.unauthorized
            message = (
                "Authorized access" if status == EventStatus.authorized else "Low confidence match"
            )
        else:
            status = EventStatus.unauthorized
            message = "Matched user not found"
    else:
        status = EventStatus.unauthorized
        message = "No matching face"

    event = AccessEvent(
        user=matched_user,
        device=device,
        status=status,
        confidence=confidence,
        snapshot_path=str(snapshot_path),
        message=message,
    )
    session.add(event)
    session.commit()
    session.refresh(event)

    alert = _maybe_create_alert(session, event)
    if alert:
        session.commit()
        session.refresh(alert)

    response = EventIngestResponse(
        event=event,
        alert=alert,
        action="unlock" if status == EventStatus.authorized else "deny",
    )

    # Broadcast to websocket subscribers
    try:
        manager.broadcast_event(response)
    except RuntimeError:
        # No active loop when running in sync context (e.g. tests)
        pass

    return response