from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

NEW = 'Новостройка'
SECONDARY = 'Вторичное'
DAY = 'День'
MONTH = 'Месяц'
YEAR = 'Год'
RENT = 'Аренда'
SELL = 'Продажа'
TL = '₺'
USD = '$'
EUR = '€'
RUB = '₽'

STATUS_CHOICES = ((NEW, 'Новостройка'), (SECONDARY, 'Вторичное'))
CURRENCY_CHOICES = ((TL, '₺'), (USD, '$'), (EUR, '€'), (RUB, '₽'))
PERIOD_CHOICES = ((DAY, 'День'), (MONTH, 'Месяц'), (YEAR, 'Год'))
SELL_TYPES = ((RENT, 'Аренда'), (SELL, 'Продажа'))


class Location(models.Model):
    """Модель локации."""

    name = models.CharField(
        max_length=100, verbose_name='Название', unique=True, db_index=True
    )

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'

    def __str__(self):
        return self.name[:15]


class PropertyType(models.Model):
    """Модель типа недвижимости."""

    name = models.CharField(
        max_length=50, verbose_name='Название', unique=True, db_index=True
    )

    class Meta:
        verbose_name = 'Тип недвижимости'
        verbose_name_plural = 'Типы недвижимости'

    def __str__(self):
        return self.name


class Facility(models.Model):
    """Модель удобств."""

    name = models.CharField(
        max_length=100, verbose_name='Название', unique=True
    )
    icon = models.SlugField(max_length=100, verbose_name='Иконка')

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

    MODEL_STRING = (
        '{name:.30} в {location} типа {type} в категории {rent_or_sell}'
    )

    title = models.CharField(max_length=200, verbose_name='Название')
    price = models.IntegerField(verbose_name='Цена')
    area = models.IntegerField(verbose_name='Площадь')
    floor = models.IntegerField(verbose_name='Этаж')
    total_floors = models.IntegerField(verbose_name='Этажность')
    construction_year = models.IntegerField(verbose_name='Год постройки')
    rooms = models.SmallIntegerField(verbose_name='Количество комнат')
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
        related_name='objects',
        db_index=True,
    )
    type = models.ForeignKey(
        PropertyType,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Тип недвижимости',
        db_index=True,
        related_name='objects',
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='objects',
        db_index=True,
        verbose_name='Владелец',
    )
    facility = models.ManyToManyField(
        Facility, related_name='objects', verbose_name='Удобства'
    )
    category = models.ForeignKey(
        Category,
        related_name='objects',
        on_delete=models.SET_NULL,
        null=True,
        db_index=True,
        verbose_name='Категория',
    )

    class Meta:
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'

    def __str__(self):
        return self.MODEL_STRING.format(
            name=self.title,
            location=self.location,
            type=self.type,
            rent_or_sell=self.category,
        )


class Image(models.Model):
    """1toМ Модель для фотографий объекта."""

    object = models.ForeignKey(
        RealEstate,
        on_delete=models.CASCADE,
        related_name='images',
        db_index=True,
        verbose_name='Объект',
    )
    image = models.ImageField(upload_to='objects', verbose_name='Фото')

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'

    def save(self, *args, **kwargs):
        # TODO: вынести в настройки, тоже самое в админке:
        if Image.objects.filter(object=self.object).count() >= 6:
            return  # Не сохраняем, если уже 6 фото
        else:
            super(Image, self).save(*args, **kwargs)


class Favorite(models.Model):
    """Модель избранного."""

    MODEL_STRING = 'Избранный объект {object.:30} пользователя {user}'

    object = models.ForeignKey(
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

    def __str__(self):
        return self.MODEL_STRING.format(
            object=self.object, user=self.user.get_username()
        )
