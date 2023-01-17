from django.contrib.auth.models import AbstractUser
from django.db import models

# from catalog.models import Location, Category, PropertyType, RealEstate

ROLE_CHOICE = (
    ('seller', 'seller'),
    ('buyer', 'buyer'),
)


# class CommonUserRequest(AbstractUser):
#     """Абстрактный класс для моделей Пользователя и Заявки."""
#     email = models.EmailField(unique=True, verbose_name='Электронная почта')
#     first_name = models.CharField(max_length=200, verbose_name='Имя')
#     last_name = models.CharField(max_length=200, verbose_name='Фамилия')
#     phone_number = models.CharField(
#         max_length=14,
#         unique=True,
#         verbose_name='Номер телефона'
#     )
#     agreement = models.BooleanField(verbose_name='Согласие', default=False)
    
#     REQUIRED_FIELDS = (
#         'email','first_name', 'last_name', 'phone_number', 'agreement'
#     )

#     class Meta:
#         abstract = True



# class CustomUser(CommonUserRequest):
class CustomUser(AbstractUser):
    """Модель пользователя."""
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    first_name = models.CharField(max_length=200, verbose_name='Имя')
    last_name = models.CharField(max_length=200, verbose_name='Фамилия')
    phone_number = models.CharField(
        max_length=14,
        unique=True,
        verbose_name='Номер телефона'
    )
    agreement = models.BooleanField(verbose_name='Согласие', default=False)
    role = models.CharField(
        max_length=6,
        choices=ROLE_CHOICE,
        default='seller'
    )
    
    REQUIRED_FIELDS = (
        'email', 'first_name', 'last_name', 'phone_number', 'agreement'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'



