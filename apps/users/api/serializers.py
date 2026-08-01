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


class ProfileSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    email = serializers.EmailField(required=False)
    name = serializers.CharField(max_length=255, required=False)
    created_at = serializers.DateTimeField(read_only=True)

    def validate(self, attrs):
        if not attrs.get("name") and not attrs.get("email"):
            raise serializers.ValidationError(
                "Informe ao menos um campo para atualizar.")
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)
