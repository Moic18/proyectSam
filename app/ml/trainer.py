from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

from app.config import get_settings
from app.ml import dataset_manager

settings = get_settings()

EMBEDDING_SIZE = 256


def extract_embedding(image_bytes: bytes, size: int = EMBEDDING_SIZE) -> List[float]:
    if not image_bytes:
        raise ValueError("Image data is empty")
    data = image_bytes[:size]
    if len(data) < size:
        data = data + bytes(size - len(data))
    return [byte / 255.0 for byte in data]


def train_model() -> Dict[int, List[float]]:
    accumulators: Dict[int, List[float]] = defaultdict(lambda: [0.0] * EMBEDDING_SIZE)
    counts: Dict[int, int] = defaultdict(int)

    for user_id, image_path in dataset_manager.iter_training_images() or []:
        embedding = extract_embedding(image_path.read_bytes())
        counts[user_id] += 1
        accumulator = accumulators[user_id]
        for idx, value in enumerate(embedding):
            accumulator[idx] += value

    if not counts:
        raise ValueError("No training images found. Please enroll faces first.")

    model: Dict[int, List[float]] = {}
    for user_id, accumulator in accumulators.items():
        total = counts[user_id]
        model[user_id] = [value / total for value in accumulator]

    settings.model_path.parent.mkdir(parents=True, exist_ok=True)
    with settings.model_path.open("w", encoding="utf-8") as fp:
        json.dump({str(user_id): vector for user_id, vector in model.items()}, fp)

    return model


def load_model() -> Dict[int, List[float]]:
    if not settings.model_path.exists():
        raise FileNotFoundError("Model file not found. Train the model first.")
    with settings.model_path.open("r", encoding="utf-8") as fp:
        data = json.load(fp)
    return {int(user_id): vector for user_id, vector in data.items()}