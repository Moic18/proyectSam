from __future__ import annotations

import secrets
from typing import Annotated, List

from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database.session import get_session
from app.ml import dataset_manager
from app.models.security import FaceEmbedding, User
from app.schemas.security import FaceEnrollmentResponse, TrainingStatusResponse, UserResponse
from app.services.face_recognition import face_service
from app.utils.security import get_password_hash

router = APIRouter(prefix="/faces", tags=["faces"])


@router.post("/enroll", response_model=FaceEnrollmentResponse)
async def enroll_face(
    background_tasks: BackgroundTasks,
    name: Annotated[str, Form(...)],
    email: Annotated[str, Form(...)],
    password: Annotated[str, Form(...)],
    files: List[UploadFile] = File(...),
    session: Session = Depends(get_session),
) -> FaceEnrollmentResponse:
    user = session.query(User).filter(User.email == email).first()
    if not user:
        user = User(name=name, email=email, hashed_password=get_password_hash(password))
        session.add(user)
        session.commit()
        session.refresh(user)

    saved = 0
    for upload in files:
        contents = await upload.read()
        filename = f"{secrets.token_hex(4)}_{upload.filename or 'face.jpg'}"
        path = dataset_manager.save_user_image(user.id, filename, contents)
        embedding = FaceEmbedding(user=user, image_path=str(path))
        session.add(embedding)
        saved += 1

    session.commit()

    background_tasks.add_task(face_service.train)

    return FaceEnrollmentResponse(user=user, images_saved=saved)


@router.get("/", response_model=List[UserResponse])
def list_users(session: Session = Depends(get_session)) -> List[UserResponse]:
    users = session.query(User).all()
    return users


@router.post("/train", response_model=TrainingStatusResponse)
def train_faces(session: Session = Depends(get_session)) -> TrainingStatusResponse:
    try:
        model = face_service.train()
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return TrainingStatusResponse(success=True, message="Model trained", total_samples=len(model))