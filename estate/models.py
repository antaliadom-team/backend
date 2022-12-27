from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

STATUS_CHOICES = ((1, 'Новостройка'), (2, 'Вторичное'))
ROOM_CHOICES = ((1, 0), (2, 1), (3, 2), (4, 3), (5, 4))
CURRENCY_CHOICES = ((1, 'usd'), (2, 'eur'), (3, 'tl'), (4, 'rub'))
PERIOD_CHOICES = ((1, 'День'), (2, 'Месяц'), (3, 'Год'))
RENT_SELL_CHOICES = ((1, 'Аренда'), (2, 'Продажа'))


class Location(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class PropertyTypes(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Facilities(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class RentSell(models.Model):
    rent_or_sell = models.CharField(max_length=20, choices=RENT_SELL_CHOICES,
                                    default='Аренда')


class Estate(models.Model):
    title = models.CharField(max_length=200)
    price = models.IntegerField()
    area = models.IntegerField()
    floor = models.IntegerField()
    total_floors = models.IntegerField()
    construction_year = models.DateField()
    rooms = models.SmallIntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES,
                              default='Новостройка')
    currency = models.CharField(max_length=20, choices=CURRENCY_CHOICES)
    description = models.TextField()
    period = models.CharField(max_length=50, choices=PERIOD_CHOICES)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL,
                                 null=True)
    type = models.ForeignKey(PropertyTypes, on_delete=models.SET_NULL,
                             null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    facilities = models.ManyToManyField(Facilities)
    rent_or_sell = models.ManyToManyField(RentSell)
    image = models.ImageField(
        upload_to='estate/images/', null=True, blank=True, default='')

    def __str__(self):
        return self.title


class Images(models.Model):
    flat = models.ForeignKey(Estate, on_delete=models.CASCADE,
                             related_name='img')
    image = models.ImageField(
        upload_to='estate/images/', verbose_name='Фото', null=True, blank=True)
