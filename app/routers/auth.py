from __future__ import annotations

from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database.session import get_session
from app.models.security import User
from app.schemas.security import Token, UserCreate, UserResponse
from app.utils.security import create_access_token, get_password_hash, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
settings = get_settings()


@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, session: Session = Depends(get_session)) -> UserResponse:
    existing = session.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = User(
        name=user.name,
        email=user.email,
        hashed_password=get_password_hash(user.password),
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_session),
) -> Token:
    user = session.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
    )
    return Token(access_token=access_token)


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_session)) -> User:
    from app.utils.security import decode_token

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_token(token)
        email: str | None = payload.get("sub")
        if email is None:
            raise credentials_exception
    except ValueError as exc:
        raise credentials_exception from exc

    user = session.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user


@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    return current_user
