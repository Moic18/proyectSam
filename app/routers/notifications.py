from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_session
from app.models.security import Alert
from app.schemas.security import AlertResponse

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("/", response_model=List[AlertResponse])
def list_alerts(session: Session = Depends(get_session)) -> List[Alert]:
    alerts = session.query(Alert).order_by(Alert.created_at.desc()).limit(50).all()
    return alerts
