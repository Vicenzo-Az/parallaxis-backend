"""
Repositório concreto do bounded context `users`.

A implementar:
- DjangoUserRepository, implementando os métodos que os use cases de
  apps/users/use_cases/*.py esperam (ex: get_by_email, save, delete).

Este é o adapter entre o ORM do Django (models.py) e os use cases, que não
devem conhecer o ORM diretamente.
"""
