from django.contrib.auth import get_user_model

from common import APITestBase
import pytest

from catalog.models import Favorite

User = get_user_model()


@pytest.mark.django_db(transaction=True)
class TestAPI(APITestBase):
    """Test API"""

    def test_favorite_object(self, user_client, favorite):
        """Test add object to favorites"""

        url = self.urls['favorite'].format(object_id=favorite.real_estate.id)
        wrong_recipe_url = self.urls['favorite'].format(object_id=999999999)

        # Get method not allowed
        self.assert_status_code(405, user_client.get(url), url=url)
        # POST of non-existent object
        self.assert_status_code(
            404, user_client.post(wrong_recipe_url), url=wrong_recipe_url
        )
        # Delete the object from favorites
        self.assert_status_code(204, user_client.delete(url), url=url)
        assert (
            Favorite.objects.count() == 0
        ), 'Объект должен быть удален из избранного'

        # Add the object to favorites
        self.assert_status_code(201, user_client.post(url), url=url)

        # Add same object twice cause 400 error
        self.assert_status_code(400, user_client.post(url), url=url)
        assert (
            Favorite.objects.count() == 1
        ), 'Объект должен быть добавлен в БД и не должен дублироваться'
        assert (
            Favorite.objects.first().user == favorite.user
        ), 'Пользователь не совпадает'
        assert (
            Favorite.objects.first().real_estate == favorite.real_estate
        ), 'Объект не совпадает'

        # Delete non-existent object from favorites
        Favorite.objects.all().delete()
        self.assert_status_code(400, user_client.delete(url), url=url)

    def test_get_categories_list(self, client, category1):
        """Test get categories"""
        response = client.get(self.urls['category_list'])
        self.assert_status_code(200, response)
        assert len(response.data) == 1, 'Количество категорий не совпадает'
        assert (
            response.data[0]['name'] == category1.name
        ), 'Название категории не совпадает'

    def test_get_categories_detail(self, client, category1):
        """Test get category detail"""
        url = self.urls['category_detail'].format(category_id=category1.id)
        response = client.get(url)
        self.assert_status_code(200, response)
        self.assert_fields(['id', 'name'], response, url=url)
        assert (
            response.data['name'] == category1.name
        ), 'Название категории не совпадает'

    def test_get_facilities_list(self, client, facility1):
        """Test get facilities"""
        response = client.get(self.urls['facility_list'])
        self.assert_status_code(200, response)
        assert len(response.data) == 1, 'Количество удобств не совпадает'
        assert (
            response.data[0]['name'] == facility1.name
        ), 'Название удобства не совпадает'

    def test_get_facilities_detail(self, client, facility1):
        """Test get facility detail"""
        url = self.urls['facility_detail'].format(facility_id=facility1.id)
        response = client.get(url)
        self.assert_status_code(200, response)
        self.assert_fields(['id', 'name'], response, url=url)
        assert (
            response.data['name'] == facility1.name
        ), 'Название удобства не совпадает'

    def test_get_locations_list(self, client, location):
        """Test get locations"""
        response = client.get(self.urls['location_list'])
        self.assert_status_code(200, response)
        assert len(response.data) == 1, 'Количество локаций не совпадает'
        assert (
            response.data[0]['name'] == location.name
        ), 'Название локации не совпадает'

    def test_get_locations_detail(self, client, location):
        """Test get location detail"""
        url = self.urls['location_detail'].format(location_slug=location.slug)
        response = client.get(url)
        self.assert_status_code(200, response)
        self.assert_fields(['id', 'name'], response, url=url)
        assert (
            response.data['name'] == location.name
        ), 'Название локации не совпадает'

    def test_get_property_types_list(self, client, property_type_apartment):
        """Test get types"""
        response = client.get(self.urls['real_estate_type_list'])
        self.assert_status_code(200, response)
        assert len(response.data) == 1, 'Количество типов не совпадает'
        assert (
            response.data[0]['name'] == property_type_apartment.name
        ), 'Название типа не совпадает'

    def test_get_property_types_detail(self, client, property_type_apartment):
        """Test get type detail"""
        url = self.urls['real_estate_type_detail'].format(
            property_type_id=property_type_apartment.id
        )
        response = client.get(url)
        self.assert_status_code(200, response)
        self.assert_fields(['id', 'name'], response, url=url)
        assert (
            response.data['name'] == property_type_apartment.name
        ), 'Название типа не совпадает'

    def test_get_real_estates_list(self, client, object1, facility1):
        """Test get real estates"""
        response = client.get(self.urls['real_estate_list'])
        self.assert_status_code(200, response)
        assert response.data['count'] == 1, 'Количество объектов не совпадает'
        assert 'results' in response.data, 'Нет ключа results'
        expected_fields = {
            'id': object1.id,
            'title': object1.title,
            'price': object1.price,
            'period': object1.period,
            'currency': object1.currency,
            'location': object1.location.id,
            'category': object1.category.id,
            'property_type': object1.property_type.id,
            'description': object1.description,
            'area': object1.area,
            'rooms': object1.rooms,
            'floor': object1.floor,
            'total_floors': object1.total_floors,
            'is_favorited': False,
            'images': [],
        }
        self.assert_fields(
            expected_fields.keys(),
            response.data['results'],
            url=self.urls['real_estate_list'],
        )
        for key, value in expected_fields.items():
            assert response.data['results'][0][key] == value, (
                f'Значение поля {key} не совпадает, ожидалось {value}, '
                f'получено {response.data["results"][0][key]}'
            )

    def test_real_estate_detail(self, client, object1):
        """Test real estate detail"""
        url = self.urls['real_estate_detail'].format(object_id=object1.id)
        response = client.get(url)
        self.assert_status_code(200, response)
        expected_fields = {
            'id': object1.id,
            'title': object1.title,
            'price': object1.price,
            'period': object1.period,
            'currency': object1.currency,
            'location': object1.location.id,
            'category': object1.category.id,
            'property_type': object1.property_type.id,
            'description': object1.description,
            'area': object1.area,
            'rooms': object1.rooms,
            'floor': object1.floor,
            'total_floors': object1.total_floors,
            'is_favorited': False,
            'images': [],
        }
        self.assert_fields(expected_fields.keys(), response, url=url)
        for key, value in expected_fields.items():
            assert response.data[key] == value, (
                f'Значение поля {key} не совпадает, ожидалось {value}, '
                f'получено {response.data[key]}'
            )

    def test_real_estate_facilities(self, client, object1, facility1):
        """Test real estate facilities"""
        url = self.urls['real_estate_detail'].format(object_id=object1.id)
        response = client.get(url)
        self.assert_status_code(200, response)
        assert (
            len(response.data['facilities']) == 1
        ), 'Количество удобств не совпадает'
        assert (
            response.data['facilities'][0]['id'] == facility1.id
        ), 'Неверный id удобства'
        assert (
            response.data['facilities'][0]['name'] == facility1.name
        ), 'Неверное название удобства'

    def test_real_estate_images(self, client, object1, image):
        """Test real estate images"""
        url = self.urls['real_estate_detail'].format(object_id=object1.id)
        response = client.get(url)
        self.assert_status_code(200, response)
        assert (
            len(response.data['images']) == 1
        ), 'Количество изображений не совпадает'
        assert (
            response.data['images'][0]['id'] == image.id
        ), 'Неверный id изображения'
        assert (
            response.data['images'][0]['image']
            == 'http://testserver/media/' + image.image.name
        ), 'Неверное изображение'
