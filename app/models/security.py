from __future__ import annotations

import enum
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class EventStatus(str, enum.Enum):
    authorized = "authorized"
    unauthorized = "unauthorized"
    unknown = "unknown"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    faces = relationship("FaceEmbedding", back_populates="user", cascade="all, delete-orphan")
    events = relationship("AccessEvent", back_populates="user")


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    token = Column(String(255), unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    events = relationship("AccessEvent", back_populates="device")


class FaceEmbedding(Base):
    __tablename__ = "face_embeddings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    image_path = Column(String(512), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="faces")


class AccessEvent(Base):
    __tablename__ = "access_events"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    status = Column(Enum(EventStatus), default=EventStatus.unknown, nullable=False)
    confidence = Column(Float, default=0.0)
    snapshot_path = Column(String(512), nullable=True)
    message = Column(Text, nullable=True)

    user = relationship("User", back_populates="events")
    device = relationship("Device", back_populates="events")
    alert = relationship("Alert", back_populates="event", uselist=False, cascade="all, delete-orphan")


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("access_events.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    message = Column(Text, nullable=False)
    resolved = Column(Boolean, default=False)

    event = relationship("AccessEvent", back_populates="alert")
