from django.conf import settings
from django.db import models

from api.validators import regex_check_number


class StaticPage(models.Model):
    """Модель статической страницы."""

    title = models.CharField(
        max_length=settings.NAMES_LENGTH, verbose_name='Заголовок'
    )
    slug = models.SlugField(
        max_length=settings.LONG_SLUG_LENGTH, verbose_name='URL'
    )
    content = models.TextField(verbose_name='Контент')
    is_active = models.BooleanField(default=True, verbose_name='Активна')

    class Meta:
        verbose_name = 'Статическая страница'
        verbose_name_plural = 'Статические страницы'

    def __str__(self):
        return self.title


class Team(models.Model):
    """Модель команды."""

    MODEL_STRING = '{first_name} {last_name} - {position}'

    first_name = models.CharField(
        max_length=settings.NAMES_LENGTH, verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=settings.NAMES_LENGTH, verbose_name='Фамилия'
    )
    phone = models.CharField(
        max_length=settings.PROPERTY_MAX_LENGTH,
        verbose_name='Телефон',
        validators=(regex_check_number,),
    )
    email = models.EmailField(verbose_name='Email')
    position = models.CharField(
        max_length=settings.NAMES_LENGTH, verbose_name='Должность'
    )
    photo = models.ImageField(upload_to='team', verbose_name='Фото')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    date_added = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата добавления'
    )

    class Meta:
        verbose_name = 'Участник команды'
        verbose_name_plural = 'Участники команды'

    def __str__(self):
        return self.MODEL_STRING.format(
            first_name=self.first_name,
            last_name=self.last_name,
            position=self.position,
        )
