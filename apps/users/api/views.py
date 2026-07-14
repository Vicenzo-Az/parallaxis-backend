"""
Views da API do bounded context `users` — RF01-RF05.

A implementar:
- RegisterView (POST /api/users/register/)
- Login e refresh: reaproveitar TokenObtainPairView / TokenRefreshView do
  simplejwt diretamente em config/urls.py, não precisa view própria.
- ProfileView (GET/PATCH /api/users/me/) — RF04
- ChangePasswordView (POST /api/users/me/change-password/) — RF05
- DeleteAccountView (DELETE /api/users/me/) — RN07

Lembrete de segurança: TODA view aqui deve declarar `permission_classes`
explicitamente, mesmo que seja igual ao default — nunca depender do
comportamento implícito (ver checklist em docs/engineering-standards.md,
item que corrige a falha real do projeto anterior).
"""
