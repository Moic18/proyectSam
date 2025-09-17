from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr

from app.models.security import EventStatus


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class FaceEnrollmentResponse(BaseModel):
    user: UserResponse
    images_saved: int


class DeviceBase(BaseModel):
    name: str
    token: str


class DeviceResponse(DeviceBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AccessEventBase(BaseModel):
    status: EventStatus
    confidence: float
    message: Optional[str]


class AccessEventCreate(BaseModel):
    device_id: int
    snapshot_path: str
    status: EventStatus
    confidence: float
    user_id: Optional[int]
    message: Optional[str]


class AccessEventResponse(BaseModel):
    id: int
    user: Optional[UserResponse]
    device: DeviceResponse
    timestamp: datetime
    status: EventStatus
    confidence: float
    snapshot_path: Optional[str]
    message: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class AlertResponse(BaseModel):
    id: int
    event: AccessEventResponse
    created_at: datetime
    message: str
    resolved: bool

    model_config = ConfigDict(from_attributes=True)


class TrainingStatusResponse(BaseModel):
    success: bool
    message: str
    total_samples: int


class EventIngestResponse(BaseModel):
    event: AccessEventResponse
    alert: Optional[AlertResponse]
    action: str