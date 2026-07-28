"""
UpdateProfileUseCase — RF04.
"""

from apps.users.domain.entities import User as DomainUser
from apps.users.domain.exceptions import EmailAlreadyRegisteredError


class UpdateProfileUseCase:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def execute(self, user_id, *, name: str | None = None, email: str | None = None) -> DomainUser:
        current_user = self.user_repository.get_by_id(user_id)

        if email is not None and email != current_user.email:
            if self.user_repository.is_email_registered(email):
                raise EmailAlreadyRegisteredError(
                    f"E-mail {email} já está registrado.")

        return self.user_repository.update(user_id, name=name, email=email)
