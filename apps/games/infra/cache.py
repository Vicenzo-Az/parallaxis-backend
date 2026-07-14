"""
Wrapper de cache do bounded context `games` (django-redis por baixo).

A implementar: funções simples de get/set com TTL de 7 dias para metadados
de jogo (RNF05), usadas pelo IGDBGameProvider antes de bater na API externa.
"""
