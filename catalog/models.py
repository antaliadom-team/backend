from datetime import datetime
import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from PIL import Image as PillowImage, ImageOps
from django_resized import ResizedImageField

from api.validators import regex_check_number

User = get_user_model()

NEW = 'Новостройка'
SECONDARY = 'Вторичное'
DAY = 'День'
MONTH = 'Месяц'
YEAR = 'Год'
RENT = 'Аренда'
# SELL = 'Продажа'
BUY = 'Покупка'
TL = '₺'
USD = '$'
EUR = '€'
RUB = '₽'

STATUS_CHOICES = ((NEW, 'Новостройка'), (SECONDARY, 'Вторичное'))
CURRENCY_CHOICES = ((TL, '₺'), (USD, '$'), (EUR, '€'), (RUB, '₽'))
PERIOD_CHOICES = ((DAY, 'День'), (MONTH, 'Месяц'), (YEAR, 'Год'))
SELL_TYPES = ((RENT, 'Аренда'), (BUY, 'Покупка'))


class Location(models.Model):
    """Модель локации."""

    name = models.CharField(
        max_length=settings.LONG_NAMES_LENGTH,
        verbose_name='Название',
        unique=True,
        db_index=True,
    )
    slug = models.SlugField(
        max_length=settings.SLUG_LENGTH, verbose_name='Слаг', unique=True
    )

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'

    def __str__(self):
        return self.name[:30]


class PropertyType(models.Model):
    """Модель типа недвижимости."""

    name = models.CharField(
        max_length=settings.PROPERTY_MAX_LENGTH,
        verbose_name='Название',
        unique=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'Тип недвижимости'
        verbose_name_plural = 'Типы недвижимости'

    def __str__(self):
        return self.name


class Facility(models.Model):
    """Модель удобств."""

    name = models.CharField(
        max_length=settings.LONG_NAMES_LENGTH,
        verbose_name='Название',
        unique=True,
    )
    icon = models.SlugField(
        max_length=settings.ICON_SLUG, verbose_name='Иконка'
    )

    class Meta:
        verbose_name = 'Удобство'
        verbose_name_plural = 'Удобства'

    def __str__(self):
        return self.name[:30]


class Category(models.Model):
    """Модель для категории объекта (аренда/продажа)."""

    name = models.CharField(
        max_length=max(len(sell_type) for _, sell_type in SELL_TYPES),
        choices=SELL_TYPES,
        default=RENT,
        unique=True,
        db_index=True,
        verbose_name='Категория объекта',
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return str(self.name)


class RealEstate(models.Model):
    """Модель объекта."""

    MODEL_STRING = '{name:.30} в {location} типа {type} в категории {category}'

    title = models.CharField(
        max_length=settings.ESTATE_TITLE_LENGTH, verbose_name='Название'
    )
    price = models.PositiveIntegerField(verbose_name='Цена')
    area = models.PositiveIntegerField(verbose_name='Площадь')
    floor = models.IntegerField(verbose_name='Этаж', null=True, blank=True)
    total_floors = models.PositiveSmallIntegerField(
        verbose_name='Этажность',
        null=True,
        blank=True,
        validators=(MinValueValidator(1),),
    )
    construction_year = models.IntegerField(
        verbose_name='Год постройки', null=True, blank=True
    )
    rooms = models.PositiveSmallIntegerField(
        verbose_name='Количество комнат',
        null=True,
        blank=True,
        validators=(MinValueValidator(1),),
    )
    date_added = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата добавления', db_index=True
    )
    status = models.CharField(
        max_length=max(len(status) for status, _ in STATUS_CHOICES),
        choices=STATUS_CHOICES,
        default=NEW,
        verbose_name='Статус',
        db_index=True,
    )
    currency = models.CharField(
        max_length=max(len(currency) for currency, _ in CURRENCY_CHOICES),
        choices=CURRENCY_CHOICES,
        default=TL,
        verbose_name='Валюта',
    )
    description = models.TextField(verbose_name='Описание')
    period = models.CharField(
        max_length=max(len(period) for period, _ in PERIOD_CHOICES),
        choices=PERIOD_CHOICES,
        default=MONTH,
        verbose_name='Период',
    )
    location = models.ForeignKey(
        Location,
        verbose_name='Локация',
        on_delete=models.SET_NULL,
        null=True,
        related_name='real_estate',
        db_index=True,
    )
    property_type = models.ForeignKey(
        PropertyType,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Тип недвижимости',
        db_index=True,
        related_name='real_estate',
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='real_estate',
        db_index=True,
        verbose_name='Владелец',
        null=True,
    )
    facility = models.ManyToManyField(
        Facility, related_name='real_estate', verbose_name='Удобства'
    )
    category = models.ForeignKey(
        Category,
        related_name='real_estate',
        on_delete=models.SET_NULL,
        null=True,
        db_index=True,
        verbose_name='Категория',
    )

    class Meta:
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'
        ordering = ('-date_added',)

    def __str__(self):
        return self.MODEL_STRING.format(
            name=self.title,
            location=self.location,
            type=self.property_type,
            category=self.category,
        )


def folder_path(instance, filename):
    """Генерирует имя файла. Возвращает путь к нему."""
    return (f'real_estate/{instance.real_estate.pk}_'
            f'{datetime.now().timestamp()*1000:.0f}.jpg')


class Image(models.Model):
    """1toМ Модель для фотографий объекта."""
    real_estate = models.ForeignKey(
        RealEstate,
        on_delete=models.CASCADE,
        related_name='images',
        db_index=True,
        verbose_name='Объект',
    )
    image = ResizedImageField(
        verbose_name='Фото',
        upload_to=folder_path,
    )

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'
        ordering = ('-id',)

    def thumbnail_generator(self, infile, outfile, image_size):
        """Генерирует изображения в требуемых размерах."""
        with PillowImage.open(infile) as im:
            im.thumbnail(image_size)
            ImageOps.fit(
                im, image_size, PillowImage.Resampling.LANCZOS, 0.5
            ).save(outfile, quality=95)

    def filename_generator(self, filepath, size):
        """Генерирует имя для каждого размера изображения."""
        width, height = size
        name, file_format = filepath.split('.')
        return f'{name}_{width}x{height}.{file_format}'

    def save(self, *args, **kwargs):
        """Сохраняет дополнительно изображения в требуемых размерах."""
        if (
            Image.objects.filter(real_estate=self.real_estate).count()
            >= settings.IMAGE_LIMIT
        ):
            return  # Не сохраняем, если уже 6 фото
        super(Image, self).save(*args, **kwargs)
        for size in settings.PREVIEW_SIZES:
            self.thumbnail_generator(
                infile=self.image,
                outfile=self.filename_generator(self.image.path, size),
                image_size=size
            )

    def delete(self, using=None, keep_parents=False):
        """Удаляет дополнительно все файлы связанные с обьектом."""
        for size in settings.PREVIEW_SIZES:
            os.remove(self.filename_generator(self.image.path, size))
        return super().delete(using, keep_parents)


class Favorite(models.Model):
    """Модель избранного."""
    real_estate = models.ForeignKey(
        RealEstate,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Объект',
        db_index=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
        db_index=True,
    )
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'real_estate'],
                name='Unique real estate with user',
            )
        ]

    def __str__(self):
        return (
            f'Избранный объект {self.real_estate.title} '
            f'пользователя {self.user.get_username()}'
        )


class Order(models.Model):
    """Модель заявки."""

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name='Аренда/Покупка'
    )
    location = models.ForeignKey(
        Location,
        related_name='orders',
        on_delete=models.SET_NULL,
        verbose_name='Локация',
        blank=True,
        null=True,
    )
    property_type = models.ForeignKey(
        PropertyType,
        on_delete=models.SET_NULL,
        verbose_name='Тип недвижимости',
        related_name='orders',
        blank=True,
        null=True,
    )
    rooms = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='Количество комнат',
        blank=True,
        null=True,
        validators=(MinValueValidator(1),),
    )
    first_name = models.CharField(
        max_length=settings.NAMES_LENGTH, verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=settings.NAMES_LENGTH, verbose_name='Фамилия'
    )
    phone = models.CharField(
        max_length=settings.PHONE_LENGTH,
        verbose_name='Номер телефона',
        validators=(regex_check_number,),
    )
    email = models.EmailField(
        verbose_name='Электронная почта', max_length=settings.EMAIL_LENGTH
    )
    comment = models.TextField(
        verbose_name='Комментарии',
        max_length=settings.COMMENT_LENGTH,
        blank=True,
        null=True,
    )
    agreement = models.BooleanField(verbose_name='Согласие', default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        related_name='orders',
        on_delete=models.CASCADE,
    )
    real_estate = models.ForeignKey(
        RealEstate,
        blank=True,
        null=True,
        related_name='orders',
        on_delete=models.CASCADE,
    )
    confirmation_code = models.CharField(
        max_length=settings.CONF_CODE_LENGTH, verbose_name='Код подтверждения.'
    )
    confirmed = models.BooleanField(
        verbose_name='Подтверждение', default=False
    )
    is_sent = models.BooleanField(verbose_name='Отправлено', default=False)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
