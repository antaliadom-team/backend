from django.db.models.signals import post_save
from django.dispatch import receiver
from djoser.signals import user_activated, user_registered

from api.metrics import (
    activated_users_counter,
    real_estate_counter,
    registered_users_counter,
)
from catalog.models import RealEstate


@receiver(user_registered)
def increment_registered_users_counter(sender, user, **kwargs):
    registered_users_counter.inc()


@receiver(user_activated)
def increment_activated_users_counter(sender, user, **kwargs):
    activated_users_counter.inc()


@receiver(post_save, sender=RealEstate)
def increment_real_estate_counter(sender, instance, created, **kwargs):
    if created:
        real_estate_counter.inc()
