import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from catalog.models import (
    Favorite,
    Location,
    PropertyType,
    Facility,
    RealEstate,
    # RentSell,
    Image,
)


User = get_user_model()

MODEL_FIELDS = [
    [
        User,
        [
            'username',
            'first_name',
            'last_name',
            'password',
            'phone',
            'email',
            'agreement',
            'role',
        ],
    ],
    [
        RealEstate,
        [
            'title',
            'price',
            'area',
            'floor',
            'total_floors',
            'construction_year',
            'rooms',
            'date_added',
            'status',
            'currency',
            'description',
            'period',
            'location_id',
            'type_id',
            'owner_id',
        ],
    ],
    [Location, ['name']],
    [PropertyType, ['name']],
    [Facility, ['name', 'icon']],
    # [RentSell, ['rent_or_sell']],
    [Image, ['object_id', 'image']],
    [Favorite, ['object_id', 'user_id']],
]

MODEL_M2M_FIELDS = [[RealEstate, ['facility', 'rent_or_sell']]]


def search_field(fields, attname):
    for field in fields:
        if attname == field.attname:
            return field
    return None


def find_verbose_name(fields):
    for field in fields:
        if field.verbose_name is not None:
            return field
        return None


@pytest.mark.django_db
class TestModels:
    @pytest.mark.parametrize(
        argnames=['model_name', 'expected_fields'], argvalues=MODEL_FIELDS
    )
    def test_model_fields(self, model_name, expected_fields):
        """Test user model specific fields"""
        model_fields = model_name._meta.fields
        for test_field in expected_fields:
            field = search_field(model_fields, test_field)
            assert (
                field is not None
            ), f'Поле {test_field} не найдено в модели {model_name}'

    @pytest.mark.parametrize(
        argnames=['model_name', 'expected_fields'], argvalues=MODEL_M2M_FIELDS
    )
    def test_model_m2m_fields(self, model_name, expected_fields):
        """Test user model m2m specific fields"""
        model_fields = model_name._meta.many_to_many
        for test_field in expected_fields:
            field = search_field(model_fields, test_field)
            assert (
                field is not None
            ), f'Поле {test_field} не найдено в модели {model_name}'

    def test_facility_constraints(self, facility1):
        """Test model Facility constraints"""
        with pytest.raises(IntegrityError):
            Facility.objects.create(name='Удобство1', icon='icon1.svg')

    def test_favorite_constraints(self, favorite, object1, user):
        """Test model Favorite constraints"""
        with pytest.raises(IntegrityError):
            Favorite.objects.create(object=object1, user=user)

    @pytest.mark.parametrize(
        argnames=['model_name', 'test_fields'], argvalues=MODEL_FIELDS
    )
    def test_fields_verbose_names(self, model_name, test_fields):
        """Test all model fields has verbose names"""
        model_fields = model_name._meta.fields
        for test_field in test_fields:
            field = search_field(model_fields, test_field)
            assert (
                field is not None
            ), f'Поле {test_field} не найдено в модели {model_name}'

    def test_is_admin_method(self, user, admin):
        """Тест атрибута is_admin модели User"""
        assert (
            user.is_admin is False
        ), 'Обычный юзер не должен обладать свойством is_admin'
        assert (
            admin.is_admin is True
        ), 'Админ с правами админа должен обладать свойством is_admin'

    def test_model_location_str(self):
        """Тест метода __str__ для модели Location"""
        model_name = Location.objects.create(name='a' * 100)
        assert (
            str(model_name) == 'a' * 15
        ), 'Имя модели Location должно содержать 15 символов'

    def test_model_property_type_str(self):
        """Тест метода __str__ для модели PropertyType"""
        model_name = PropertyType.objects.create(name='u' * 50)
        assert (
            str(model_name) == 'u' * 50
        ), 'Имя модели PropertyType должно содержать все 50 символов'

    def test_model_facility_str(self):
        """Тест метода __str__ для модели Facility"""

        model_name = Facility.objects.create(name='a' * 100, icon='icon1.svg')
        assert (
            str(model_name) == 'a' * 30
        ), 'Имя модели Facility должно содержать не более 30 символов'

    def test_model_favorite_str(self, user, object1):
        """Тест метода __str__ для модели Favorite"""
        favorite = Favorite.objects.create(object=object1, user=user)
        assert (
            str(favorite)
            == f'Избранный объект Тестовый объект 1 пользователя test_user'
        )

    def test_model_object_str(self, property_type_apartment, location):
        """Тест метода __str__ для модели Object"""
        model_name = RealEstate.objects.create(
            name='a' * 100,
            type=property_type_apartment,
            location=location,
            rent_or_sell=1,
        )
        assert (
            str(model_name)
            == 'a' * 30
            + ' в Тестовая локация типа Квартира в категории Аренда'
        ), 'Имя модели Object некорректно'
