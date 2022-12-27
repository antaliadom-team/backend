from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

STATUS_CHOICES = ((1, 'Новостройка'), (2, 'Вторичное'))
CURRENCY_CHOICES = (
    ('USD', 'USD'),
    ('EUR', 'EUR'),
    ('TL', 'TL'),
    ('RUB', 'RUB'),
)
PERIOD_CHOICES = ((1, 'День'), (2, 'Месяц'), (3, 'Год'))
RENT_SELL_CHOICES = ((1, 'Аренда'), (2, 'Продажа'))


class Location(models.Model):
    """Модель локации"""

    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'

    def __str__(self):
        return self.name


class PropertyType(models.Model):
    """Модель типа недвижимости"""
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Тип недвижимости'
        verbose_name_plural = 'Типы недвижимости'

    def __str__(self):
        return self.name


class Facility(models.Model):
    """Модель удобств"""
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Удобство'
        verbose_name_plural = 'Удобства'

    def __str__(self):
        return self.name


class RentSell(models.Model):
    """М2М Модель для аренды/продажи"""
    rent_or_sell = models.IntegerField(
        choices=RENT_SELL_CHOICES,
        default=1,
    )

    def __str__(self):
        return self.rent_or_sell


class Images(models.Model):
    """М2М Модель для фотографий объекта"""
    image = models.ImageField(upload_to='estate/images/', verbose_name='Фото')

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'


class Object(models.Model):
    """Модель объекта"""

    MODEL_STRING = (
        '{name:.30} в {location} типа {type} в категории {rent_or_sell}'
    )

    title = models.CharField(max_length=200)
    price = models.IntegerField()
    area = models.IntegerField()
    floor = models.IntegerField()
    total_floors = models.IntegerField()
    construction_year = models.IntegerField()
    rooms = models.SmallIntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    currency = models.CharField(
        max_length=max(len(currency) for _, currency in CURRENCY_CHOICES),
        choices=CURRENCY_CHOICES,
    )
    description = models.TextField()
    period = models.IntegerField(choices=PERIOD_CHOICES, default=1)
    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True
    )
    type = models.ForeignKey(
        PropertyType, on_delete=models.SET_NULL, null=True
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    facility = models.ManyToManyField(Facility)
    rent_or_sell = models.ManyToManyField(RentSell)
    image = models.ManyToManyField(Images)

    class Meta:
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'

    def __str__(self):
        return self.MODEL_STRING.format(
            name=self.name,
            location=self.location,
            type=self.type,
            rent_or_sell=self.rent_or_sell,
        )
