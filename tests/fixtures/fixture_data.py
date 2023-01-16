import pytest

from catalog.models import (
    Favorite,
    Location,
    PropertyType,
    Facility,
    RealEstate,
)
# TODO: дополнить фикстурами из моделей юзера
# from users.models import BuyerRequest


@pytest.fixture
def location():
    return Location.objects.create(name='Тестовая локация')


@pytest.fixture
def location2():
    return Location.objects.create(name='Другая тестовая локация')


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
def object1(user, facility1, property_type_villa, location):

    recipe = RealEstate.objects.create(
        name='Тестовый объект 1'
    )
    recipe.facility.add(facility1)
    return recipe


@pytest.fixture
def favorite(user, object1):
    return Favorite.objects.create(object=object1, user=user)


@pytest.fixture
def image_str():
    return (
        'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYA'
        'AAAfFcSJAAAADUlEQVR42mNk+P+/HgAFhAJ/wlseKgAAAABJRU5ErkJggg'
        '=='
    )
