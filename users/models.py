from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.db import models
from django.conf import settings
from phone_field import PhoneField

from .managers import UserManager

ROLE_CHOICE = (
    ('seller', 'seller'),
    ('buyer', 'buyer'),
)

class CustomUser(AbstractUser):
    """Модель пользователя."""
    username = None
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    first_name = models.CharField(max_length=200, verbose_name='Имя')
    last_name = models.CharField(max_length=200, verbose_name='Фамилия')
    phone_number = models.CharField(max_length=14, unique=True, verbose_name='Номер телефона')
    agreement = models.BooleanField(verbose_name='Согласие', default=False)
    role = models.CharField(max_length=6, choices=ROLE_CHOICE, default='seller')
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number', 'agreement']

    objects = UserManager()
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

# class Favorites(models.Model):
#     follower = models.ForeignKey(CustomUser, related_name='favorites', on_delete=models.CASCADE)
#     real_estate = models.ForeignKey('Estate',)