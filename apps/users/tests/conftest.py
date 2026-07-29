import pytest

from apps.users.tests.fakes import FakeUserRepository


@pytest.fixture
def existing_user():
    fake_repo = FakeUserRepository()
    user = fake_repo.create(email="john@example.com",
                            name="John", password="senha123")
    return fake_repo, user
