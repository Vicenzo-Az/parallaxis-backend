from uuid import uuid4

from django.utils import timezone

from apps.users.domain.entities import User as DomainUser
from apps.users.domain.exceptions import UserNotFoundError


class FakeUserRepository:
    def __init__(self):
        self._users = {}
        self._passwords = {}

    def is_email_registered(self, email: str) -> bool:
        return any(user.email == email for user in self._users.values())

    def create(self, email: str, name: str, password: str):
        user = DomainUser(
            id=uuid4(),
            email=email,
            name=name,
            created_at=timezone.now()
        )
        self._users[user.id] = user
        self._passwords[user.id] = password
        return user

    def get_by_id(self, user_id) -> DomainUser:
        try:
            return self._users[user_id]
        except KeyError:
            raise UserNotFoundError(
                f"Usuário com id {user_id} não encontrado.") from None

    def update(self, user_id, *, name=None, email=None) -> DomainUser:
        try:
            user = self._users[user_id]
        except KeyError:
            raise UserNotFoundError(
                f"Usuário com id {user_id} não encontrado.") from None

        if email is not None:
            user.email = email
        if name is not None:
            user.name = name
        if name is not None or email is not None:
            self._users[user_id] = user

        return user

    def verify_password(self, user_id, password: str) -> bool:
        if user_id not in self._users:
            raise UserNotFoundError(
                f"Usuário com id {user_id} não encontrado.")
        return self._passwords.get(user_id) == password

    def set_password(self, user_id, new_password: str) -> None:
        if user_id not in self._users:
            raise UserNotFoundError(
                f"Usuário com id {user_id} não encontrado.")
        self._passwords[user_id] = new_password
