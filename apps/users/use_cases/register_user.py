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
