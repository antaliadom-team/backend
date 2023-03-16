from django.conf import settings
from django.contrib.auth import get_user_model, password_validation
from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework import serializers

from api.validators import regex_check_number, validate_name

User = get_user_model()


class BaseUserSerializer(serializers.ModelSerializer):
    """Базовый клас сериализатора пользователей"""

    def validate_phone(self, value):
        return regex_check_number(value)

    def validate_first_name(self, value):
        return validate_name(value)

    def validate_last_name(self, value):
        return validate_name(value)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'first_name',
            'last_name',
            'phone',
            'agreement',
        )


class RegisterUserSerializer(BaseUserSerializer):
    """Сериализатор создания пользователей."""

    re_password = serializers.CharField(
        max_length=settings.PASSWORD_LENGTH,
        write_only=True,
        help_text='Введите пароль повторно.',
    )
    phone = serializers.CharField()
    agreement = serializers.BooleanField()

    def validate_agreement(self, value):
        if not value:
            raise serializers.ValidationError(
                'Вы должны принять соглашение о конфиденциальности.'
            )
        return value

    def validate(self, data):
        """Проверяет, что password_confirmation - password равны."""
        super().validate(data)
        if data['re_password'] != data['password']:
            raise ValidationError(
                {
                    'password_error': (
                        'Повторный пароль не совпадает с оригинальным.'
                    )
                }
            )

        data.pop('re_password', None)
        password = data.pop('password', None)
        user = User(**data)
        try:
            password_validation.validate_password(password, user)
        except ValidationError as e:
            raise serializers.ValidationError(
                {'password': serializers.as_serializer_error(e)}
            )
        return data

    def create(self, validated_data):
        with transaction.atomic():
            user = User(
                first_name=self.validated_data['first_name'],
                last_name=self.validated_data['last_name'],
                email=self.validated_data['email'],
                phone=self.validated_data['phone'],
                agreement=self.validated_data['agreement'],
            )
            user.set_password(self.initial_data['password'])
            user.save()
            return user

    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + (
            'password',
            're_password',
            'agreement',
        )
        extra_kwargs = {'password': {'write_only': True, 'required': True}}


class UserSerializer(BaseUserSerializer):
    """Сериализатор пользователей."""

    class Meta(BaseUserSerializer.Meta):
        read_only_fields = ('email', 'agreement')
