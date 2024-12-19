from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class PasswordField(serializers.CharField):
    """Дефолтные настройки для поля с паролем."""
    def __init__(self, **kwargs):
        kwargs.setdefault('write_only', True)
        kwargs.setdefault('required', True)
        kwargs.setdefault('min_length', 8)
        kwargs.setdefault('style', {'input_type': 'password'})
        super().__init__(**kwargs)


class RegisterSerializer(serializers.ModelSerializer):
    """Сериалайзер для регистрации пользователя (JWT не предусмотрен)."""
    password = PasswordField()
    password_confirm = PasswordField()

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name',
            'email', 'password', 'password_confirm'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError(
                {'password_confirm': 'Пароли не совпадают.'}
            )
        return attrs

    def create(self, validated_data: dict):
        validated_data.pop('password_confirm')
        return User.objects.create_user(**validated_data)
