"""
Model Django do bounded context `users`.

A implementar:
- User(AbstractBaseUser ou extensão do model padrão do Django) mapeando para
  a tabela `users` do MER (docs/database-model.md): id (UUID, PK), email
  (UNIQUE), password_hash, name, created_at.

Lembrete: este é o único lugar do bounded context onde "Django" e "regra de
negócio" se encontram — é por isso que fica isolado em infra/, e não em
domain/ ou use_cases/.
"""
