from rest_framework import serializers
from rest_framework.validators import UniqueValidator, ValidationError
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
        if value[0] == '+':
            if len(value) < 12:
                raise ValidationError('Номер слишком короткий!')
            self.number_check(value=value, start=1)
        else:
            if len(value) < 10:
                raise ValidationError('Номер слишком короткий!')
            self.number_check(value=value, start=0)
        return value
    
    def number_check(self, value, start):
        for i in range(start, len(value)):
                try:
                    int(value[i])
                except ValueError:
                    raise ValidationError(
                        'Номер телефона должен состоять из чисел.'
                    )

