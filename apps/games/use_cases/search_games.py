"""
SearchGamesUseCase — RF06, RF07.

A implementar:
- Recebe uma query e um GameDataProvider injetado (nunca instanciado aqui).
- Retorna resultados já normalizados para as entidades de domain/entities.py.
- Não sabe e não deve saber se o provider por trás é IGDB, RAWG, ou um fake
  de teste — essa é a essência do ADR004.
"""
