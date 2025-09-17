from __future__ import annotations

from pathlib import Path
from typing import Generator, Iterable, Tuple

from app.config import get_settings

settings = get_settings()

def get_user_dir(user_id: int) -> Path:
    user_dir = settings.dataset_dir / str(user_id)
    user_dir.mkdir(parents=True, exist_ok=True)
    return user_dir


def save_user_image(user_id: int, filename: str, data: bytes) -> Path:
    user_dir = get_user_dir(user_id)
    path = user_dir / filename
    path.write_bytes(data)
    return path


def iter_training_images() -> Generator[Tuple[int, Path], None, None]:
    if not settings.dataset_dir.exists():
        return
    for user_dir in settings.dataset_dir.iterdir():
        if not user_dir.is_dir():
            continue
        try:
            user_id = int(user_dir.name)
        except ValueError:
            continue
        for image_path in user_dir.glob("*.jpg"):
            yield user_id, image_path
        for image_path in user_dir.glob("*.png"):
            yield user_id, image_path