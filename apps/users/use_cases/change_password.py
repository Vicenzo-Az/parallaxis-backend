"""
ChangePasswordUseCase — RF05.
"""

from apps.users.domain.exceptions import InvalidCredentialsError, SamePasswordError


class ChangePasswordUseCase:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def execute(self, user_id, *, old_password: str, new_password: str) -> None:
        if not self.user_repository.verify_password(user_id, old_password):
            raise InvalidCredentialsError("Invalid old password.")

        if old_password == new_password:
            raise SamePasswordError(
                "New password cannot be the same as the old password."
            )

        self.user_repository.set_password(user_id, new_password)
