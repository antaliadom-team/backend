from rest_framework import serializers
from rest_framework.validators import UniqueValidator, ValidationError
from rest_framework.generics import get_object_or_404
from django.contrib.auth import get_user_model


User = get_user_model()


class MyDjoserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя."""
    agreement = serializers.BooleanField()
    username = serializers.CharField(
        max_length=200,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        max_length=200,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    phone_number = serializers.CharField(
        max_length=14,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        write_only_fields = ('username',)
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'password',
            'agreement',
            'role',
        )
        model = User
    
    
    def create(self, validated_data):
        validated_data['username'] = validated_data['email']
        user = User.objects.create_user(**validated_data)
        return user
    
    def validate_phone_number(self, value):
        if len(value) < 10:
            raise ValidationError('Номер слишком короткий!')
        return value

# Делал разделение администратора и CustomUser. Убрал из модели USERNAME_FIELD
# пытался сделать токен отдельно для CustomUser. Но не находит пользователя.
class TokenSerializer(serializers.Serializer):# это все не работает.
    """Сериализатор для получения токена."""
    email = serializers.EmailField(
        source='username',
        max_length=250,
        write_only=True,
    )
    password = serializers.CharField(
        max_length=255,
        write_only=True
    )

    class Meta:
        fields = ('username', 'password')


    def validate(self, data):
        # user = get_object_or_404(User, email=data['email'])
        user = get_object_or_404(User, email=data['username'])
        
        user_1 = User.objects.filter(
            # email=user.email,
            email=user.username,
            password=data['password']
        ).exists()
        if not user_1:
            raise serializers.ValidationError(
                'Такого пользователя нет.'
            )
        return data
