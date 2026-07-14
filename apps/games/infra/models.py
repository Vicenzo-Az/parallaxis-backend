"""
Models Django do bounded context `games`.

A implementar, mapeando fielmente docs/database-model.md:
- Game (UUID PK, igdb_id UNIQUE, ratings 0-100 com CheckConstraint)
- Genre (UUID PK, name UNIQUE)
- LibraryEntry (UUID PK, FK user CASCADE, FK game RESTRICT, UNIQUE
  (user, game) para RN01, CheckConstraint de score 1-10 e de score
  condicional ao status para RN02)

Lembrete: as CheckConstraint do Meta.constraints são a aplicação real das
regras de negócio no nível de banco — não é redundante com a validação do
use case, é uma segunda linha de defesa (defesa em profundidade).
"""
