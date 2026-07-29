"""
Exceções de domínio do bounded context `users`.

A implementar, por exemplo:
- EmailAlreadyRegisteredError
- InvalidCredentialsError

Essas exceções são capturadas na camada `api/views.py` e traduzidas para o
status HTTP apropriado — a camada de domínio não sabe o que é um status HTTP.
"""


class InvalidCredentialsError(Exception):
    """Levantada ao tentar acessar com credenciais inválidas (RN de autenticação)."""


class EmailAlreadyRegisteredError(Exception):
    """Levantada ao tentar registrar um e-mail que já existe (RN de unicidade)."""


class UserNotFoundError(Exception):
    """Levantada ao tentar acessar um usuário que não existe (RN de existência)."""


class SamePasswordError(Exception):
    """Levantada ao tentar alterar a senha para a mesma senha antiga (RN de alteração de senha)."""
