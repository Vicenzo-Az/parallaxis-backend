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

from apps.users.domain.exceptions import (
    EmailAlreadyRegisteredError,
    InvalidCredentialsError,
    SamePasswordError,
    UserNotFoundError,
)
from apps.users.tests.fakes import FakeUserRepository
from apps.users.use_cases.change_password import ChangePasswordUseCase
from apps.users.use_cases.register_user import RegisterUserUseCase
from apps.users.use_cases.update_profile import UpdateProfileUseCase

# RegisterUserUseCase

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


# UpdateProfileUseCase

def test_update_profile_changes_name(existing_user):
    fake_repo, user = existing_user

    use_case = UpdateProfileUseCase(user_repository=fake_repo)
    updated = use_case.execute(user.id, name="John Updated")

    assert updated.name == "John Updated"


def test_update_profile_changes_email_when_available(existing_user):
    fake_repo, user = existing_user

    use_case = UpdateProfileUseCase(user_repository=fake_repo)
    updated = use_case.execute(user.id, email="john@updated.com")

    assert updated.email == "john@updated.com"


def test_update_profile_raises_when_new_email_already_registered(existing_user):
    fake_repo, user = existing_user
    fake_repo.create(email="taken@example.com",
                     name="Other User", password="senha456")

    use_case = UpdateProfileUseCase(user_repository=fake_repo)

    with pytest.raises(EmailAlreadyRegisteredError):
        use_case.execute(user.id, email="taken@example.com")

    assert user.email == "john@example.com"


def test_update_profile_allows_keeping_same_email(existing_user):
    # este é o teste que prova que a armadilha do e-mail duplicado
    # está genuinamente resolvida — não é opcional, é o teste mais
    # importante desse use case
    fake_repo, user = existing_user

    use_case = UpdateProfileUseCase(user_repository=fake_repo)
    updated = use_case.execute(user.id, email="john@example.com")

    assert updated.email == "john@example.com"


def test_update_profile_raises_when_user_not_found(existing_user):
    fake_repo, user = existing_user

    use_case = UpdateProfileUseCase(user_repository=fake_repo)

    with pytest.raises(UserNotFoundError):
        use_case.execute(user_id=999, name="New Name")


# ChangePasswordUseCase

def test_change_password_succeeds_with_correct_old_password(existing_user):
    fake_repo, user = existing_user

    use_case = ChangePasswordUseCase(user_repository=fake_repo)
    use_case.execute(user.id, old_password="senha123",
                     new_password="nova_senha456")

    assert fake_repo.verify_password(user.id, "nova_senha456")


def test_change_password_raises_when_old_password_is_wrong(existing_user):
    fake_repo, user = existing_user

    use_case = ChangePasswordUseCase(user_repository=fake_repo)

    with pytest.raises(InvalidCredentialsError):
        use_case.execute(user.id, old_password="senha_errada",
                         new_password="nova_senha456")


def test_change_password_raises_when_new_password_equals_old(existing_user):
    fake_repo, user = existing_user

    use_case = ChangePasswordUseCase(user_repository=fake_repo)

    with pytest.raises(SamePasswordError):
        use_case.execute(user.id, old_password="senha123",
                         new_password="senha123")
