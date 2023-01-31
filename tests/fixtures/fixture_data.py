import pytest

from about.models import Team, StaticPage
from catalog.models import (
    Favorite,
    Location,
    PropertyType,
    Facility,
    RealEstate,
    Category,
)

# TODO: дополнить фикстурами из моделей юзера
# from users.models import BuyerRequest


@pytest.fixture
def location():
    return Location.objects.create(
        name='Тестовая локация', slug='test-location'
    )


@pytest.fixture
def location2():
    return Location.objects.create(
        name='Другая тестовая локация', slug='another-test-location'
    )


@pytest.fixture
def property_type_apartment():
    return PropertyType.objects.create(name='Квартира')


@pytest.fixture
def property_type_villa():
    return PropertyType.objects.create(name='Вилла')


@pytest.fixture
def facility1():
    return Facility.objects.create(name='Удобство1', icon='icon1.svg')


@pytest.fixture
def facility2():
    return Facility.objects.create(name='Удобство2', icon='icon2.svg')


@pytest.fixture
def category1():
    return Category.objects.create(name='Аренда')


@pytest.fixture
def object1(user, facility1, property_type_villa, location, category1):

    real_estate = RealEstate.objects.create(
        title='Тестовый объект 1',
        type=property_type_villa,
        location=location,
        category=category1,
        price=1000000,
        area=100,
    )
    real_estate.facility.add(facility1)
    return real_estate


@pytest.fixture
def favorite(user, object1):
    return Favorite.objects.create(real_estate=object1, user=user)


@pytest.fixture
def image_str():
    return (
        'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYA'
        'AAAfFcSJAAAADUlEQVR42mNk+P+/HgAFhAJ/wlseKgAAAABJRU5ErkJggg'
        '=='
    )


@pytest.fixture
def static_page():
    return StaticPage.objects.create(
        title='Тестовая страница', content='Тестовый контент', slug='test-page'
    )


@pytest.fixture
def team_member1(image_str):
    return Team.objects.create(
        position='Должность1',
        phone='+79999999999',
        email='team1@fake.mail',
        first_name='Имя1',
        last_name='Фамилия1',
        photo=image_str,
    )
