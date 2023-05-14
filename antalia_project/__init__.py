from django.apps import apps

from .celery import app as celery_app

__all__ = ('celery_app',)


def register_signals():
    if apps.ready and not apps.signals_ready:
        apps.setup()
        apps.signals_ready = True


register_signals()
