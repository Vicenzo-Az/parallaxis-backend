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
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.api.serializers import RegisterSerializer
from apps.users.domain.exceptions import EmailAlreadyRegisteredError
from apps.users.infra.repositories import DjangoUserRepository
from apps.users.use_cases.register_user import RegisterUserUseCase


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(request=RegisterSerializer, responses={201: None})
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = RegisterUserUseCase(user_repository=DjangoUserRepository())
        try:
            user = use_case.execute(**serializer.validated_data)
        except EmailAlreadyRegisteredError:
            return Response(
                {"email": "Já existe uma conta com este e-mail."},
                status=status.HTTP_409_CONFLICT,
            )

        response_data = {
            "id": user.id,
            "email": user.email,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
