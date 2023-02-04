import factory
from django.contrib.auth import get_user_model
from faker import Faker

from catalog.models import (
    Category,
    Location,
    PropertyType,
    RealEstate,
)

faker = Faker(locale='TR_tr')

User = get_user_model()


class RealEstateFactory(factory.django.DjangoModelFactory):
    """Фабрика для модели RealEstate."""

    title = factory.LazyAttribute(
        lambda x: '{} по адресу {}'.format(
            faker.random_element(
                [
                    f'Прекрасный {x.property_type.name} со своим бассейном',
                    f'Уютный {x.property_type.name}',
                    f'Видовой {x.property_type.name} в новом комплексе',
                    f'Элегантный {x.property_type.name}',
                    f'Просторный {x.property_type.name}',
                    f'Светлый и уютный {x.property_type.name}',
                ]
            ),
            faker.address(),
        )
    )
    description = factory.Faker('text', max_nb_chars=300)
    price = factory.Faker('pyint', min_value=1_000, max_value=1_000_000)
    area = factory.Faker('pyint', min_value=40, max_value=1_000)
    rooms = factory.Faker('pyint', min_value=1, max_value=6)
    floor = factory.Faker('pyint', min_value=1, max_value=10)
    total_floors = factory.Faker('pyint', min_value=1, max_value=10)
    construction_year = factory.Faker('pyint', min_value=1960, max_value=2027)
    status = factory.Faker(
        'random_element', elements=('Новостройка', 'Вторичное')
    )
    currency = factory.Faker('random_element', elements=('₺', '$', '€', '₽'))
    period = factory.Faker('random_element', elements=('День', 'Месяц', 'Год'))
    location = factory.Iterator(Location.objects.all())
    property_type = factory.Iterator(PropertyType.objects.all())
    category = factory.Iterator(Category.objects.all())
    owner = factory.Iterator(User.objects.filter(is_superuser=True))

    class Meta:
        model = RealEstate
