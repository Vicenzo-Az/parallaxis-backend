"""
Serializers do bounded context `users`.

A implementar: RegisterSerializer, ProfileSerializer, ChangePasswordSerializer.
Toda validação de formato (ex: força mínima de senha, formato de e-mail) vive
aqui — validação de regra de negócio (ex: e-mail já cadastrado) vive no use
case, não aqui.
"""
from rest_framework import serializers


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    name = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True, min_length=8)
