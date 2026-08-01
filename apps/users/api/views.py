"""
Views da API do bounded context `users` — RF01-RF05.

"""
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.api.serializers import (
    ChangePasswordSerializer,
    DeleteAccountSerializer,
    ProfileSerializer,
    RegisterSerializer,
)
from apps.users.domain.exceptions import (
    EmailAlreadyRegisteredError,
    InvalidCredentialsError,
    SamePasswordError,
)
from apps.users.infra.repositories import DjangoUserRepository
from apps.users.use_cases.change_password import ChangePasswordUseCase
from apps.users.use_cases.delete_account import DeleteAccountUseCase
from apps.users.use_cases.register_user import RegisterUserUseCase
from apps.users.use_cases.update_profile import UpdateProfileUseCase


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


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=ProfileSerializer)
    def get(self, request):
        repository = DjangoUserRepository()
        user = repository.get_by_id(request.user.id)

        serializer = ProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=ProfileSerializer, responses=ProfileSerializer)
    def patch(self, request):
        serializer = ProfileSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        use_case = UpdateProfileUseCase(user_repository=DjangoUserRepository())

        try:
            updated_user = use_case.execute(
                user_id=request.user.id,
                name=serializer.validated_data.get("name"),
                email=serializer.validated_data.get("email"),
            )
        except EmailAlreadyRegisteredError:
            return Response(
                {"email": "Já existe uma conta com este e-mail."},
                status=status.HTTP_409_CONFLICT,
            )

        response_serializer = ProfileSerializer(updated_user)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=DeleteAccountSerializer, responses={204: None})
    def delete(self, request):
        serializer = DeleteAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = DeleteAccountUseCase(user_repository=DjangoUserRepository())

        try:
            use_case.execute(
                user_id=request.user.id,
                password=serializer.validated_data["password"],
            )
        except InvalidCredentialsError:
            return Response(
                {"password": "Senha incorreta."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(request=ChangePasswordSerializer, responses={204: None})
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = ChangePasswordUseCase(
            user_repository=DjangoUserRepository())

        try:
            use_case.execute(
                user_id=request.user.id,
                old_password=serializer.validated_data["old_password"],
                new_password=serializer.validated_data["new_password"],
            )
        except InvalidCredentialsError:
            return Response(
                {"old_password": "Senha atual incorreta."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except SamePasswordError:
            return Response(
                {"new_password": "A nova senha não pode ser igual à atual."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)
