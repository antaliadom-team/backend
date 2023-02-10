import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from about.models import StaticPage, Team
from catalog.models import (
    Favorite,
    Location,
    PropertyType,
    Facility,
    RealEstate,
    Image,
    Order,
    Category,
)


User = get_user_model()

MODEL_FIELDS = [
    [
        User,
        [
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
            'property_type_id',
            'owner_id',
        ],
    ],
    [
        Order,
        [
            'category_id',
            'location_id',
            'property_type_id',
            'rooms',
            'first_name',
            'last_name',
            'phone',
            'email',
            'comment',
            'agreement',
            'date_added',
            'real_estate_id',
        ],
    ],
    [Category, ['name']],
    [Location, ['name']],
    [PropertyType, ['name']],
    [Facility, ['name', 'icon']],
    [Image, ['real_estate_id', 'image']],
    [Favorite, ['real_estate_id', 'user_id']],
    [StaticPage, ['title', 'content', 'slug', 'is_active']],
    [
        Team,
        [
            'first_name',
            'last_name',
            'phone',
            'email',
            'position',
            'photo',
            'date_added',
            'is_active',
        ],
    ],
]

MODEL_M2M_FIELDS = [[RealEstate, ['facility']]]


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
            Favorite.objects.create(real_estate=object1, user=user)

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

    def test_model_location_str(self):
        """Тест метода __str__ для модели Location"""
        model_name = Location.objects.create(name='a' * 100)
        assert (
            str(model_name) == 'a' * 30
        ), 'Имя модели Location должно содержать 30 символов'

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
        favorite = Favorite.objects.create(real_estate=object1, user=user)
        assert str(favorite) == (
            f'Избранный объект Тестовый объект 1 пользователя '
            f'test.user@fake.mail'
        )

    def test_model_real_estate_str(
        self, property_type_apartment, location, category1
    ):
        """Тест метода __str__ для модели RealEstate"""
        model_name = RealEstate.objects.create(
            title='a' * 100,
            property_type=property_type_apartment,
            location=location,
            category=category1,
            price=100000,
            area=100,
        )
        assert (
            str(model_name)
            == 'a' * 30
            + ' в Тестовая локация типа Квартира в категории Аренда'
        ), 'Имя модели RealEstate некорректно'

    def test_model_category_str(self):
        """Тест метода __str__ для модели Category"""
        model_name = Category.objects.create(name='a' * 50)
        assert (
            str(model_name) == 'a' * 50
        ), 'Имя модели Category должно содержать все 50 символов'

    def test_model_staticpage_str(self):
        """Тест метода __str__ для модели StaticPages"""
        model_name = StaticPage.objects.create(title='a' * 50)
        assert (
            str(model_name) == 'a' * 50
        ), 'Имя модели StaticPages должно содержать все 50 символов'

    def test_model_team_str(self, team_member1):
        """Тест метода __str__ для модели Team"""
        model_name = team_member1.__str__()
        assert model_name, 'Имя1 Фамилия1 - Должность1'

    def test_model_image_limit(self, object1):
        """Тест количества изображений для модели RealEstate"""
        for i in range(1, settings.IMAGE_LIMIT + 2):
            Image.objects.create(real_estate=object1, image=f'image{i}.jpg')
        assert (
            Image.objects.filter(real_estate=object1).count()
            == settings.IMAGE_LIMIT
        ), 'Максимальное количество изображений для объекта недвижимости'

    def test_model_user_str(self, user):
        """Тест метода __str__ для модели User"""
        assert (
            str(user) == 'Tester Testerson (test.user@fake.mail)'
        ), 'Неверно формируется имя экземпляра объекта User'
        assert user.get_short_name() == 'Tester', 'Неверно формируется имя'
        assert (
            user.get_full_name() == 'Tester Testerson'
        ), 'Неверно формируется полное имя'
