"""
DeleteAccountUseCase — RN07.

A implementar:
- Remove o usuário, o que deve disparar cascade delete de todos os
  LibraryEntry associados (configurado via on_delete=CASCADE no model,
  ver docs/database-model.md).
- Não afeta registros de Game (cache compartilhado, não é dado pessoal).
"""
