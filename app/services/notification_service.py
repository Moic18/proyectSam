from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List


@dataclass
class NotificationMessage:
    subject: str
    body: str


class NotificationService:
    """Simplified notification service that logs messages.

    In a production system you would integrate with Telegram, email or SMS. For
    demonstration purposes we simply store the messages in memory so they can be
    inspected and, optionally, sent elsewhere later on.
    """

    def __init__(self) -> None:
        self.sent_notifications: List[NotificationMessage] = []

    def send(self, message: NotificationMessage) -> None:
        self.sent_notifications.append(message)

    def list_notifications(self) -> Iterable[NotificationMessage]:
        return list(self.sent_notifications)


notification_service = NotificationService()
