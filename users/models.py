from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from api.validators import regex_check_number, validate_name
from users.managers import CustomUserManager

ROLE_CHOICE = (('seller', 'seller'), ('buyer', 'buyer'))


class User(AbstractUser):
    """Модель пользователя."""

    username = None
    email = models.EmailField(
        max_length=settings.EMAIL_LENGTH,
        unique=True,
        verbose_name='Электронная почта',
        error_messages={
            'unique': (
                'Пользоватль с таким адресом электронной '
                'почты уже существует.'
            )
        },
    )
    first_name = models.CharField(
        max_length=settings.NAMES_LENGTH,
        verbose_name='Имя',
        validators=(validate_name,),
    )
    last_name = models.CharField(
        max_length=settings.NAMES_LENGTH,
        verbose_name='Фамилия',
        validators=(validate_name,),
    )
    phone = models.CharField(
        max_length=settings.PHONE_LENGTH,
        unique=False,
        verbose_name='Номер телефона',
        validators=(regex_check_number,),
    )
    agreement = models.BooleanField(verbose_name='Согласие', default=False)
    role = models.CharField(
        max_length=settings.USER_ROLE_LENGTH,
        choices=ROLE_CHOICE,
        default='seller',
    )

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-id',)

    def __str__(self):
        return f'{self.get_full_name()} ({self.email})'

    def get_username(self):
        return self.email

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
