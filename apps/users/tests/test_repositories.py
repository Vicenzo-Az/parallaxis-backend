"""
Testes de integração do bounded context `users` — DjangoUserRepository.

Diferente de test_use_cases.py, estes testes tocam o banco de dados real
(via @pytest.mark.django_db) — são a validação de que o adapter concreto
cumpre o mesmo contrato que FakeUserRepository simula nos testes de use case.
"""
from uuid import uuid4

import pytest

from apps.users.domain.entities import User as DomainUser
from apps.users.domain.exceptions import UserNotFoundError
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

    assert django_user.password != "testpassword"
    assert django_user.check_password("testpassword")


# get_by_id

@pytest.mark.django_db
def test_get_by_id_returns_domain_user(existing_django_user):
    user = DjangoUserRepository().get_by_id(existing_django_user.id)

    assert isinstance(user, DomainUser)
    assert user.id == existing_django_user.id
    assert user.email == existing_django_user.email
    assert user.name == existing_django_user.name


@pytest.mark.django_db
def test_get_by_id_raises_when_user_not_found():
    with pytest.raises(UserNotFoundError):
        DjangoUserRepository().get_by_id(uuid4())


# update

@pytest.mark.django_db
def test_update_changes_name_in_database(existing_django_user):
    DjangoUserRepository().update(existing_django_user.id, name="Novo Nome")

    refreshed = DjangoUser.objects.get(id=existing_django_user.id)
    assert refreshed.name == "Novo Nome"


@pytest.mark.django_db
def test_update_changes_email_in_database(existing_django_user):
    DjangoUserRepository().update(existing_django_user.id, email="newemail@example.com")

    refreshed = DjangoUser.objects.get(id=existing_django_user.id)
    assert refreshed.email == "newemail@example.com"


@pytest.mark.django_db
def test_update_raises_when_user_not_found():
    with pytest.raises(UserNotFoundError):
        DjangoUserRepository().update(uuid4(), name="Novo Nome")


# verify_password / set_password

@pytest.mark.django_db
def test_verify_password_returns_true_for_correct_password(existing_django_user):
    assert DjangoUserRepository().verify_password(
        existing_django_user.id, "testpassword")


@pytest.mark.django_db
def test_verify_password_returns_false_for_wrong_password(existing_django_user):
    assert not DjangoUserRepository().verify_password(
        existing_django_user.id, "wrongpassword")


@pytest.mark.django_db
def test_set_password_updates_hash_in_database(existing_django_user):
    DjangoUserRepository().set_password(existing_django_user.id, "newpassword")

    refreshed = DjangoUser.objects.get(id=existing_django_user.id)

    assert refreshed.password != "newpassword"
    assert refreshed.check_password("newpassword")


# delete

@pytest.mark.django_db
def test_delete_removes_user_from_database(existing_django_user):
    DjangoUserRepository().delete(existing_django_user.id)

    with pytest.raises(UserNotFoundError):
        DjangoUserRepository().get_by_id(existing_django_user.id)

    assert not DjangoUser.objects.filter(id=existing_django_user.id).exists()


@pytest.mark.django_db
def test_delete_raises_when_user_not_found():
    with pytest.raises(UserNotFoundError):
        DjangoUserRepository().delete(uuid4())
