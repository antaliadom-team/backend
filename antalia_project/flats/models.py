from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

STATUS_CHOICES = ((1, 'Новостройка'), (2, 'Вторичное'))
AREA_CHOICES = ((1, 'Анталия'), (2, 'Стамбул'), (3, 'Северный Кипр'))
TYPE_CHOICES = ((1, 'Участок'), (2, 'Студия'), (3, 'Квартира'), (4, 'Вилла'),)
ROOM_CHOICES = ((1, 0), (2, 1), (3, 2), (4, 3), (5, 4))


class Flat(models.Model):
    title = models.CharField(max_length=250)
    price = models.IntegerField()
    area = models.IntegerField()
    floor = models.IntegerField()
    year = models.IntegerField()
    desc = models.TextField()
    image = models.ImageField(
        upload_to='flats/images/', null=True, blank=True, default='')

    def __str__(self):
        return self.title


class Images(models.Model):
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE,
                             related_name='img')
    image = models.ImageField(
        upload_to='flats/images/', verbose_name='Фото', null=True, blank=True)


class Rent(models.Model):
    title = models.CharField(max_length=250)
    area = models.CharField(max_length=50, choices=AREA_CHOICES)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    room = models.IntegerField(choices=ROOM_CHOICES)
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE,
                             related_name='rent')


class Buy(models.Model):
    title = models.CharField(max_length=250)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES)
    area = models.CharField(max_length=50, choices=AREA_CHOICES)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    room = models.IntegerField(choices=ROOM_CHOICES)
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE,
                             related_name='buy')
