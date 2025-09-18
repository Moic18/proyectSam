from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.database.session import session_scope
from app.models.security import Device, User
from app.utils.security import get_password_hash


def main() -> None:
    with session_scope() as session:
        if not session.query(User).filter(User.email == "admin@example.com").first():
            session.add(
                User(
                    name="Administrator",
                    email="admin@example.com",
                    hashed_password=get_password_hash("admin"),
                )
            )
        if not session.query(Device).filter(Device.token == "demo-device").first():
            session.add(Device(name="Front Door", token="demo-device"))


if __name__ == "__main__":
    main()
