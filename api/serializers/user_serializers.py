from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from django.contrib.auth import get_user_model

from djoser.serializers import UserSerializer  as DjoserUserSerializer

from users.models import CustomUser

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Для пользователя."""

    class Meta:
        model = CustomUser
        fields = (
        'id',
        'email',
        'first_name',
        'last_name',
        'phone_number',
        'password',
        'agreement',
        'role',

        )


class TokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена."""
    email = serializers.EmailField(
        max_length=250,
        write_only=True,
    )
    password = serializers.CharField(
        max_length=255,
        write_only=True
    )

    def validate(self, data):
        user = get_object_or_404(CustomUser, email=data['email'])
        user_1 = CustomUser.objects.filter(
            email=user.email,
            password=data['password']
        ).exists()
        if not user_1:
            raise serializers.ValidationError(
                'Такого пользователя нет.'
            )
        return data


class MyDjoserSerializer(DjoserUserSerializer):
    agreement = serializers.BooleanField()

    class Meta:
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'password',
            'agreement',
            'role',
        )
        model = User
    
    # def validated_data(self):
    #     return 
