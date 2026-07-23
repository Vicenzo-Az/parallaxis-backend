"""
Testes de integração do bounded context `users` — DjangoUserRepository.

Diferente de test_use_cases.py, estes testes tocam o banco de dados real
(via @pytest.mark.django_db) — são a validação de que o adapter concreto
cumpre o mesmo contrato que FakeUserRepository simula nos testes de use case.
"""
import pytest

from apps.users.domain.entities import User as DomainUser
from apps.users.infra.models import User as DjangoUser
from apps.users.infra.repositories import DjangoUserRepository


@pytest.mark.django_db
def test_is_email_registered_returns_false_for_unknown_email():
    assert not DjangoUserRepository().is_email_registered("unknown@example.com")


@pytest.mark.django_db
def test_is_email_registered_returns_true_after_create():
    DjangoUserRepository().create(
        email="test@example.com", name="Test User", password="testpassword"
    )
    assert DjangoUserRepository().is_email_registered("test@example.com")


@pytest.mark.django_db
def test_create_returns_domain_user_not_django_model():
    user = DjangoUserRepository().create(
        email="test@example.com",
        name="Test User",
        password="testpassword"
    )
    assert isinstance(user, DomainUser)


@pytest.mark.django_db
def test_create_persists_user_with_hashed_password():
    DjangoUserRepository().create(
        email="test@example.com",
        name="Test User",
        password="testpassword"
    )

    django_user = DjangoUser.objects.get(email="test@example.com")
    assert django_user.password != "testpassword"  # password should be hashed
    # check_password should return True
    assert django_user.check_password("testpassword")
