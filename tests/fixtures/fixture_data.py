from django.core.files.uploadedfile import SimpleUploadedFile

import pytest

from about.models import StaticPage, Team
from catalog.models import (
    Category,
    Facility,
    Favorite,
    Image,
    Location,
    PropertyType,
    RealEstate,
)


@pytest.fixture
def image_str():
    return (
        'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYA'
        'AAAfFcSJAAAADUlEQVR42mNk+P+/HgAFhAJ/wlseKgAAAABJRU5ErkJggg'
        '=='
    )


@pytest.fixture
def image_path():
    return '/backend_media/test_path.jpg'


@pytest.fixture
def image(object1):
    image = SimpleUploadedFile(
        name='test_image.jpg',
        content=b'file_content',
        content_type='image/jpeg',
    )
    return Image.objects.create(image=image, real_estate=object1)


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
def category2():
    return Category.objects.create(name='Продажа')


@pytest.fixture
def object1(user, facility1, property_type_villa, location, category1):

    real_estate = RealEstate.objects.create(
        title='Тестовый объект 1',
        property_type=property_type_villa,
        location=location,
        category=category1,
        price=1000000,
        area=100,
    )
    real_estate.facility.add(facility1)
    return real_estate


@pytest.fixture
def object2(user, facility1, property_type_apartment, location, category2):

    real_estate = RealEstate.objects.create(
        title='Тестовый объект 2 - продажа',
        property_type=property_type_apartment,
        location=location,
        category=category2,
        price=1000000,
        area=100,
    )
    real_estate.facility.add(facility1)
    return real_estate


@pytest.fixture
def favorite(user, object1):
    return Favorite.objects.create(real_estate=object1, user=user)


@pytest.fixture
def static_page():
    return StaticPage.objects.create(
        title='Тестовая страница', content='Тестовый контент', slug='test-page'
    )


@pytest.fixture
def team_member1(image_path):
    return Team.objects.create(
        position='Должность1',
        phone='+79999999999',
        email='team1@fake.mail',
        first_name='Имя1',
        last_name='Фамилия1',
        photo=image_path,
    )
