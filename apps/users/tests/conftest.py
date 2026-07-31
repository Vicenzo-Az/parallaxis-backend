import pytest

from apps.users.infra.repositories import DjangoUserRepository
from apps.users.tests.fakes import FakeUserRepository


@pytest.fixture
def existing_user():
    fake_repo = FakeUserRepository()
    user = fake_repo.create(email="john@example.com",
                            name="John", password="senha123")
    return fake_repo, user


@pytest.fixture
def existing_django_user():
    return DjangoUserRepository().create(
        email="test@example.com", name="Test User", password="testpassword"
    )
