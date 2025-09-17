from __future__ import annotations

import math
from typing import Dict, List, Optional, Tuple

from app.ml import trainer


class FaceRecognitionService:
    def __init__(self) -> None:
        self.model: Dict[int, List[float]] = {}

    def load(self) -> None:
        try:
            self.model = trainer.load_model()
        except FileNotFoundError:
            self.model = {}

    def is_ready(self) -> bool:
        return bool(self.model)

    def predict(self, image_bytes: bytes) -> Tuple[Optional[int], float]:
        if not self.is_ready():
            return None, 0.0

        embedding = trainer.extract_embedding(image_bytes)
        best_user: Optional[int] = None
        best_distance = math.inf

        for user_id, vector in self.model.items():
            distance = self._euclidean_distance(embedding, vector)
            if distance < best_distance:
                best_distance = distance
                best_user = user_id

        if best_user is None:
            return None, 0.0

        confidence = 1.0 / (1.0 + best_distance)
        return best_user, confidence

    def train(self) -> Dict[int, List[float]]:
        self.model = trainer.train_model()
        return self.model

    @staticmethod
    def _euclidean_distance(a: List[float], b: List[float]) -> float:
        return math.sqrt(sum((ax - bx) ** 2 for ax, bx in zip(a, b)))


face_service = FaceRecognitionService()
