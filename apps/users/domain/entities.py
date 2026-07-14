"""
Entidades puras do bounded context `users` — sem import de Django.

A implementar (ver docs/domain-model.md):
- User: id, email, name, created_at (password_hash fica só na camada infra,
  nunca deve trafegar como atributo de entidade de domínio em texto claro).

Lembrete de arquitetura (ADR001): este módulo não pode importar nada de
`django.*`, `rest_framework.*` ou `apps.users.infra.*`. Se sentir necessidade
de importar Django aqui, é sinal de que a lógica pertence à camada infra, não
a esta.
"""
