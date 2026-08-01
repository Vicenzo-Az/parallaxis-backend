"""
DeleteAccountUseCase — RN07.

- Remove o usuário, o que deve disparar cascade delete de todos os
  LibraryEntry associados (configurado via on_delete=CASCADE no model,
  ver docs/database-model.md).
- Não afeta registros de Game (cache compartilhado, não é dado pessoal).
"""


from apps.users.domain.exceptions import InvalidCredentialsError


class DeleteAccountUseCase:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def execute(self, user_id, *, password: str) -> None:
        if not self.user_repository.verify_password(user_id, password):
            raise InvalidCredentialsError("Senha incorreta.")

        self.user_repository.delete(user_id)
