from __future__ import annotations

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
