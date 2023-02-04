import random

from django.conf import settings
from django.core.management.base import BaseCommand

from catalog.models import Facility, Image
from tests.factories.realestate_factory import RealEstateFactory


class Command(BaseCommand):
    help = (
        'Генерирует множество объектов модели RealEstate при помощи '
        'RealEstateFactory.'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            'total',
            type=int,
            help=(
                'Задает количество объектов модели RealEstate, которое нужно '
                'создать.'
            ),
        )

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        existing_images = Image.objects.all()
        real_estates = [RealEstateFactory() for _ in range(total)]
        for real_estate in real_estates:
            real_estate.facility.set(
                [
                    random.choice(Facility.objects.all())
                    for _ in range(random.randint(2, 7))
                ]
            )
            real_estate.save()

        image_instances = [
            Image(
                real_estate=real_estate,
                image=random.choice(existing_images).image,
            )
            for real_estate in real_estates
            for _ in range(random.randint(1, settings.NUM_IMAGES))
        ]
        Image.objects.bulk_create(image_instances)

        for real_estate in real_estates:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Объект {real_estate.title} был создан успешно!'
                )
            )
