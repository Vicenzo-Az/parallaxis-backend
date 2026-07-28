"""
Repositório concreto do bounded context `users`.

A implementar:
- DjangoUserRepository, implementando os métodos que os use cases de
  apps/users/use_cases/*.py esperam (ex: get_by_email, save, delete).

Este é o adapter entre o ORM do Django (models.py) e os use cases, que não
devem conhecer o ORM diretamente.
"""
from apps.users.domain.entities import User as DomainUser
from apps.users.domain.exceptions import UserNotFoundError
from apps.users.infra.models import User as DjangoUser


class DjangoUserRepository:
    def is_email_registered(self, email: str) -> bool:
        return DjangoUser.objects.filter(email=email).exists()

    def create(self, email: str, name: str, password: str) -> DomainUser:
        django_user = DjangoUser.objects.create_user(
            email=email,
            name=name,
            password=password
        )
        return self._to_domain(django_user)

    def get_by_id(self, user_id) -> DomainUser:
        try:
            django_user = DjangoUser.objects.get(id=user_id)
        except DjangoUser.DoesNotExist:
            raise UserNotFoundError(
                f"Usuário com id {user_id} não encontrado.") from None

        return self._to_domain(django_user)

    def update(self, user_id, *, name: str | None = None, email: str | None = None) -> DomainUser:
        try:
            django_user = DjangoUser.objects.get(id=user_id)
        except DjangoUser.DoesNotExist:
            raise UserNotFoundError(
                f"Usuário com id {user_id} não encontrado.") from None

        if email is not None:
            django_user.email = email
        if name is not None:
            django_user.name = name
        if email is not None or name is not None:
            django_user.save()

        return self._to_domain(django_user)

    def verify_password(self, user_id, password: str) -> bool:
        try:
            django_user = DjangoUser.objects.get(id=user_id)
        except DjangoUser.DoesNotExist:
            raise UserNotFoundError(
                f"Usuário com id {user_id} não encontrado.") from None

        return django_user.check_password(password)

    def set_password(self, user_id, new_password: str) -> None:
        try:
            django_user = DjangoUser.objects.get(id=user_id)
        except DjangoUser.DoesNotExist:
            raise UserNotFoundError(
                f"Usuário com id {user_id} não encontrado.") from None

        django_user.set_password(new_password)
        django_user.save()

    def _to_domain(self, django_user: DjangoUser) -> DomainUser:
        return DomainUser(
            id=django_user.id,
            email=django_user.email,
            name=django_user.name,
            created_at=django_user.created_at,
        )
