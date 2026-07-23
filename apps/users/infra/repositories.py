"""
Repositório concreto do bounded context `users`.

A implementar:
- DjangoUserRepository, implementando os métodos que os use cases de
  apps/users/use_cases/*.py esperam (ex: get_by_email, save, delete).

Este é o adapter entre o ORM do Django (models.py) e os use cases, que não
devem conhecer o ORM diretamente.
"""
from apps.users.domain.entities import User as DomainUser
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
        return DomainUser(
            id=django_user.id,
            email=django_user.email,
            name=django_user.name,
            created_at=django_user.created_at,
        )
