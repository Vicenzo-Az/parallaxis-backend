"""
RegisterUserUseCase — RF01.

A implementar:
- Recebe email/senha/nome já validados pelo serializer.
- Verifica unicidade de e-mail (RN: users.email UNIQUE).
- Delega hashing de senha e persistência ao repositório (infra).
- Levanta EmailAlreadyRegisteredError se e-mail já existir.

Lembrete de teste (RNF07a): este use case deve ser testável injetando um
repositório fake em memória, sem precisar de banco de dados real.
"""


from apps.users.domain.entities import User
from apps.users.domain.exceptions import EmailAlreadyRegisteredError


class RegisterUserUseCase:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def execute(self, email: str, name: str, password: str) -> "User":
        # Verifica se o e-mail já está registrado
        if self.user_repository.is_email_registered(email):
            raise EmailAlreadyRegisteredError(
                f"E-mail {email} já está registrado.")

        # Cria um novo usuário com a senha hashada
        new_user = self.user_repository.create(
            email=email, name=name, password=password)

        return new_user
