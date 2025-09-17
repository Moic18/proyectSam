from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DB_PATH = BASE_DIR / "security.db"
DEFAULT_MODEL_PATH = BASE_DIR / "ml" / "embeddings" / "face_model.json"
DEFAULT_DATASET_DIR = BASE_DIR / "ml" / "data"
DEFAULT_STORAGE_DIR = BASE_DIR / "storage" / "events"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        protected_namespaces=("settings_",),
    )

    app_name: str = Field("Smart Security API", env="APP_NAME")
    secret_key: str = Field("change-this-secret", env="SECRET_KEY")
    access_token_expire_minutes: int = Field(60 * 24, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    algorithm: str = Field("HS256", env="ALGORITHM")

    database_url: str = Field(f"sqlite:///{DEFAULT_DB_PATH}", env="DATABASE_URL")

    model_path: Path = Field(DEFAULT_MODEL_PATH, env="MODEL_PATH")
    dataset_dir: Path = Field(DEFAULT_DATASET_DIR, env="DATASET_DIR")
    storage_dir: Path = Field(DEFAULT_STORAGE_DIR, env="STORAGE_DIR")

    jwt_token_prefix: str = Field("Bearer", env="JWT_TOKEN_PREFIX")
    face_match_threshold: float = Field(0.45, env="FACE_MATCH_THRESHOLD")


@lru_cache()
def get_settings() -> Settings:
    settings = Settings()
    settings.model_path.parent.mkdir(parents=True, exist_ok=True)
    settings.dataset_dir.mkdir(parents=True, exist_ok=True)
    settings.storage_dir.mkdir(parents=True, exist_ok=True)
    return settings