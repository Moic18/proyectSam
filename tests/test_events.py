from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import get_settings
from app.models.security import Base, Device, EventStatus
from app.services.event_service import process_event


def _create_image_bytes(value: int) -> bytes:
    return bytes([value] * 512)


def setup_database(tmp_path):
    settings = get_settings()
    settings.dataset_dir = tmp_path / "data"
    settings.dataset_dir.mkdir(parents=True, exist_ok=True)
    settings.storage_dir = tmp_path / "storage"
    settings.storage_dir.mkdir(parents=True, exist_ok=True)
    settings.model_path = tmp_path / "model.json"

    engine = create_engine("sqlite://", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(bind=engine, future=True)
    Base.metadata.create_all(bind=engine)
    return engine, TestingSessionLocal


def test_process_event_without_model(tmp_path):
    engine, SessionLocal = setup_database(tmp_path)
    session: Session = SessionLocal()

    device = Device(name="Test", token="token")
    session.add(device)
    session.commit()

    image_bytes = _create_image_bytes(0)
    response = process_event(session, device_token="token", image_bytes=image_bytes)

    assert response.event.status in {EventStatus.unauthorized, EventStatus.unknown}
    assert response.action == "deny"

    session.close()
    engine.dispose()
