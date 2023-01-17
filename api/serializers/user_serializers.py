from rest_framework import serializers
from rest_framework.validators import UniqueValidator, ValidationError
from django.contrib.auth import get_user_model

# from users.models import Order
# from users.models import CustomUser as User

User = get_user_model()

class MyDjoserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя."""
    agreement = serializers.BooleanField()
    username = serializers.CharField(
        max_length=200,
        validators=[UniqueValidator(queryset=User.objects.all())],
        write_only=True
    )
    email = serializers.EmailField(
        max_length=200,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    phone_number = serializers.CharField(
        max_length=14,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(max_length=128, write_only=True)
    password_again = serializers.CharField(
        max_length=128,
        write_only=True,
        help_text='Введите пароль повторно.'
    )

    class Meta:
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'password',
            'password_again',
            'agreement',
            'role',
        )
        model = User
    
    
    def create(self, validated_data):
        """
        Заполняет поле username полем email.
        Создает пользователя.
        """
        validated_data['username'] = validated_data['email']
        user = User.objects.create_user(**validated_data)
        return user
    
    def validate(self, data):
        """
        Проверяет, что password_again - password равны.
        Удаляет из словаря поле password_again
        """
        super().validate(data)
        if data['password_again'] != data['password']:
            raise ValidationError(
                'Повторный пароль не совпадает с оригинальным!'
            )
        
        data.pop('password_again', None)
        return data
    
    def validate_password_again(self, value):
        """Проверяет, что повторный пароль не пустой."""
        if value == '':
            raise ValidationError(
                'Поле повторный пароль не может быть пустым!'
            )
        return value
    
    def validate_phone_number(self, value):
        """
        Проверяет длину номера телефона и добавляет знак '+',
        если он отсутстует.
        """
        if value[0] == '+':
            if len(value) < 12:
                raise ValidationError('Номер слишком короткий!')
            self._number_check(value=value, start=1)
        else:
            if len(value) < 10:
                raise ValidationError('Номер слишком короткий!')
            self._number_check(value=value, start=0)
            return '+' + value 
        return value
    
    def _number_check(self, value, start):
        """Проверяет чтоб номер телефона состоял из цифр."""
        for i in range(start, len(value)):
                try:
                    int(value[i])
                except ValueError:
                    raise ValidationError(
                        'Номер телефона должен состоять из чисел.'
                    )
