from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models

ROLE_CHOICE = (('seller', 'seller'), ('buyer', 'buyer'))


class User(AbstractUser):
    """Модель пользователя."""

    email = models.EmailField(
        max_length=settings.EMAIL_LENGTH, unique=True,
        verbose_name='Электронная почта')
    first_name = models.CharField(max_length=settings.NAMES_LENGTH,
                                  verbose_name='Имя')
    last_name = models.CharField(max_length=settings.NAMES_LENGTH,
                                 verbose_name='Фамилия')
    phone_number = models.CharField(
        max_length=settings.PHONE_LENGTH,
        unique=True, verbose_name='Номер телефона')
    agreement = models.BooleanField(verbose_name='Согласие', default=False)
    role = models.CharField(
        max_length=settings.USER_ROLE_LENGTH,
        choices=ROLE_CHOICE, default='seller')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-id',)
