"""
Testes de use cases do bounded context `users` — RNF07a.

Rodam sem banco de dados real: toda dependência de infra é substituída por
um fake (ver fakes.py), isolando a regra de negócio pura do use case.

Padrão Arrange-Act-Assert:
- Arrange: instancia FakeUserRepository() e RegisterUserUseCase(user_repository=...).
- Act: chama .execute(...).
- Assert: verifica o resultado.
"""
import pytest

from apps.users.domain.exceptions import EmailAlreadyRegisteredError
from apps.users.tests.fakes import FakeUserRepository
from apps.users.use_cases.register_user import RegisterUserUseCase


def test_register_user_creates_user_with_valid_data():
    fake_user_repository = FakeUserRepository()
    register_user_use_case = RegisterUserUseCase(
        user_repository=fake_user_repository)

    user = register_user_use_case.execute(
        email="john.doe@example.com", name="John Doe", password="password123"
    )

    assert user.email == "john.doe@example.com"
    assert user.name == "John Doe"
    assert user.created_at is not None
    assert user.id is not None
    assert fake_user_repository.is_email_registered("john.doe@example.com")


def test_register_user_raises_when_email_already_registered():
    fake_user_repository = FakeUserRepository()
    register_user_use_case = RegisterUserUseCase(
        user_repository=fake_user_repository)
    register_user_use_case.execute(
        email="john.doe@example.com", name="John Doe", password="password123"
    )

    with pytest.raises(EmailAlreadyRegisteredError):
        register_user_use_case.execute(
            email="john.doe@example.com", name="John Doe", password="password123"
        )


def test_register_user_allows_different_email_after_duplicate_rejection():
    fake_user_repository = FakeUserRepository()
    register_user_use_case = RegisterUserUseCase(
        user_repository=fake_user_repository)
    register_user_use_case.execute(
        email="john.doe@example.com", name="John Doe", password="password123"
    )
    with pytest.raises(EmailAlreadyRegisteredError):
        register_user_use_case.execute(
            email="john.doe@example.com", name="John Doe", password="password123"
        )

    user = register_user_use_case.execute(
        email="jane.doe@example.com", name="Jane Doe", password="password123"
    )

    assert user.email == "jane.doe@example.com"
    assert fake_user_repository.is_email_registered("jane.doe@example.com")
