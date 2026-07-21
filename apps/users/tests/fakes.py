from uuid import uuid4

from django.utils import timezone

from apps.users.domain.entities import User as DomainUser


class FakeUserRepository:
    def __init__(self):
        self._users = {}

    def is_email_registered(self, email: str) -> bool:
        return email in self._users

    def create(self, email: str, name: str, password: str):
        user = DomainUser(
            id=uuid4(),
            email=email,
            name=name,
            created_at=timezone.now()
        )
        self._users[email] = user
        return user
