from __future__ import annotations

import argparse

from app.services.face_recognition import face_service


def main() -> None:
    parser = argparse.ArgumentParser(description="Train the face recognition model")
    parser.parse_args()
    model = face_service.train()
    print(f"Model trained for {len(model)} users")


if __name__ == "__main__":
    main()
