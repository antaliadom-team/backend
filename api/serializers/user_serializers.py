from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from django.contrib.auth import get_user_model
from antalia_project.settings import ACCOUNT_USER_MODEL_USERNAME_FIELD


User = get_user_model()

# Нужно скопировать поле email в поле username  и возможно отрезать до собачки.

class MyDjoserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя."""
    agreement = serializers.BooleanField()

    class Meta:
        write_only_fields = ('username',)
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

# Делал разделение администратора и CustomUser. Убрал из модели USERNAME_FIELD
# пытался сделать токен отдельно для CustomUser. Но не находит пользователя.
class TokenSerializer(serializers.Serializer):# это все не работает.
    """Сериализатор для получения токена."""
    email = serializers.EmailField(
        max_length=250,
        write_only=True,
    )
    password = serializers.CharField(
        max_length=255,
        write_only=True
    )
    # username = serializers.CharField(
    #     max_length=255,
    #     write_only=True
    # )

    def validate(self, data):
        # ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'
        user = get_object_or_404(User, email=data['email'])
        
        user_1 = User.objects.filter(
            email=user.email,
            password=data['password']
        ).exists()
        if not user_1:
            raise serializers.ValidationError(
                'Такого пользователя нет.'
            )
        return data
