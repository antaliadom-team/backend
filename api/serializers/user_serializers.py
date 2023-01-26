from django.contrib.auth import get_user_model, password_validation
from django.core.exceptions import ValidationError
from django.db import transaction
from django.conf import settings
from rest_framework import serializers

User = get_user_model()


class BaseUserSerializer(serializers.ModelSerializer):
    """Базовый клас сериализатора пользователей"""

    class Meta:
        model = User
        fields = ('email', 'id', 'first_name', 'last_name')


class RegisterUserSerializer(BaseUserSerializer):
    """Сериализатор создания пользователей."""

    password_confirmation = serializers.CharField(
        # TODO: вынести max-length в settings
        max_length=settings.PASSWORD_LENGTH,
        write_only=True, help_text='Введите пароль повторно.')
    phone_number = serializers.CharField(max_length=settings.PHONE_LENGTH)
    agreement = serializers.BooleanField()

    def validate(self, data):
        """Проверяет, что password_confirmation - password равны."""
        # TODO: По-моему такой метод есть в djoser, надо посмотреть
        super().validate(data)
        if data['password_confirmation'] != data['password']:
            raise ValidationError(
                'Повторный пароль не совпадает с оригинальным!'
            )

        data.pop('password_confirmation', None)
        data.pop('password', None)
        return data

    def validate_password(self, data):
        password = data
        errors = None
        try:
            password_validation.validate_password(password=password)
        except ValidationError as e:
            errors = list(e.messages)
        if errors:
            raise serializers.ValidationError(errors)
        return super().validate(data)

    def create(self, validated_data):
        with transaction.atomic():
            user = User(
                username=self.initial_data['email'],
                first_name=self.initial_data['first_name'],
                last_name=self.initial_data['last_name'],
                email=self.initial_data['email'],
            )
            user.set_password(self.initial_data['password'])
            user.save()
            return user

    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + (
            'password',
            'password_confirmation',
            'phone_number',
            'agreement',
        )
        extra_kwargs = {'password': {'write_only': True, 'required': True}}


class UserSerializer(BaseUserSerializer):
    """Сериализатор пользователей."""
