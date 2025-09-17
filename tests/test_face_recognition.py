from __future__ import annotations

from app.ml import trainer


def test_extract_embedding_shape():
    data = bytes([255] * 128)
    embedding = trainer.extract_embedding(data)

    assert len(embedding) == 256
    assert embedding[0] == 1.0
    assert embedding[-1] == 0.0
