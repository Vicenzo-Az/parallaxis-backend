"""
RateGameUseCase — RF08-RF12.

A implementar:
- Cria ou atualiza um LibraryEntry para (user_id, game_id).
- Aplica RN01 (unicidade), RN02 (score obrigatório condicional ao status),
  RN06/RN03 (atualiza rated_at a cada edição), RN08 (limite de review).
- É o use case com maior densidade de regra de negócio do projeto — merece
  a maior atenção de teste (ver M2 em docs/mvp-roadmap.md).
"""
