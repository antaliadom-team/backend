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
        wrong_object_url = self.urls['favorite'].format(object_id=999999999)

        # Get method not allowed
        self.assert_status_code(405, user_client.get(url), url=url)
        # POST of non-existent object
        self.assert_status_code(
            404, user_client.post(wrong_object_url), url=wrong_object_url
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
        url = self.urls['location_detail'].format(location_id=location.id)
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

    def test_real_estate_is_not_favorited(self, client, object1):
        """Test real estate favorites for anonymous user"""
        url = self.urls['real_estate_detail'].format(object_id=object1.id)
        response = client.get(url)
        self.assert_status_code(200, response)
        assert (
            response.data['is_favorited'] is False
        ), 'Неверное значение is_favorited. Для анонимов должно быть false.'

    def test_real_estate_is_favorited(self, user_client, object1, favorite):
        """Test real estate favorites"""
        url = self.urls['real_estate_detail'].format(object_id=object1.id)
        response = user_client.get(url)
        self.assert_status_code(200, response)
        assert (
            response.data['is_favorited'] is True
        ), 'Неверное значение is_favorited'

    def test_real_estate_list_is_favorited(
        self, user_client, object1, object2, favorite
    ):
        """Test real estate favorites"""
        url = self.urls['real_estate_list']
        response = user_client.get(url)
        self.assert_status_code(200, response)
        for i in range(len(response.data['results'])):
            if response.data['results'][i]['id'] == object1.id:
                assert (
                    response.data['results'][i]['is_favorited'] is True
                ), f'Неверное значение is_favorited для объекта {object1.id}'
            else:
                assert (
                    response.data['results'][i]['is_favorited'] is False
                ), f'Неверное значение is_favorited для объекта {object2.id}'

    def test_real_estate_list_filter_by_favorite(
        self, user_client, object1, object2, favorite
    ):
        """Test real estate favorites. Filter by favorite"""
        url = self.urls['real_estate_list']
        response = user_client.get(url, {'is_favorited': True})
        self.assert_status_code(200, response)
        assert (
            len(response.data['results']) == 1
        ), 'Неверное количество объектов, должен быть 1 объект в избранном.'
        assert (
            response.data['results'][0]['id'] == object1.id
        ), f'Неверный объект. Должен быть объект с {object1.id}'

    def test_real_estate_list_filter_by_rooms(self, client, object1, object2):
        """Test real estate list filter by rooms"""
        url = self.urls['real_estate_list']
        response = client.get(url, {'rooms': object1.rooms})
        self.assert_status_code(200, response)
        assert (
            len(response.data['results']) == 1
        ), 'Неверное количество объектов, должен быть 1 объект с 1 комнатой.'
        assert (
            response.data['results'][0]['id'] == object1.id
        ), f'Неверный объект. Должен быть объект с {object1.id}'

    def test_real_estate_list_filter_by_rooms_4(
        self, client, object1, object2, object_rooms4, object_rooms5
    ):
        """Test real estate list filter by rooms. 4+ rooms"""
        url = self.urls['real_estate_list']
        response = client.get(url, {'rooms': 4})
        self.assert_status_code(200, response)
        assert len(response.data['results']) == 2, (
            'Неверное количество объектов, должен быть 2 объекта с 4+ '
            'комнатами.'
        )

    def test_real_estate_list_filter_by_category(
        self, client, object1, object2
    ):
        """Test real estate list filter by category"""
        url = self.urls['real_estate_list']
        response = client.get(url, {'category': object1.category.id})
        self.assert_status_code(200, response)
        assert len(response.data['results']) == 1, (
            f'Неверное количество объектов, должен быть 1 объект с '
            f'категорией {object1.category.id}.'
        )
        assert (
            response.data['results'][0]['id'] == object1.id
        ), f'Неверный объект. Должен быть объект с {object1.id}'

    def test_real_estate_list_filter_by_type(self, client, object1, object2):
        """Test real estate list filter by type"""
        url = self.urls['real_estate_list']
        response = client.get(url, {'property_type': object1.property_type.id})
        self.assert_status_code(200, response)
        assert len(response.data['results']) == 1, (
            f'Неверное количество объектов, должен быть 1 объект с '
            f'типом {object1.property_type.id}.'
        )
        assert (
            response.data['results'][0]['id'] == object1.id
        ), f'Неверный объект. Должен быть объект с {object1.id}'

    def test_real_estate_list_filter_by_location(
        self, client, object1, object2
    ):
        """Test real estate list filter by location"""
        url = self.urls['real_estate_list']
        response = client.get(url, {'location': object1.location.id})
        self.assert_status_code(200, response)
        assert len(response.data['results']) == 1, (
            f'Неверное количество объектов, должен быть 1 объект с '
            f'типом {object1.location.id}.'
        )
        assert (
            response.data['results'][0]['id'] == object1.id
        ), f'Неверный объект. Должен быть объект с {object1.id}'

    def test_real_estate_list_multiple_filters(
        self, client, object1, object2, object_rooms5, object3
    ):
        """Test real estate list with multiple filters"""
        url = self.urls['real_estate_list']
        response = client.get(
            url,
            {
                'category': object1.category.id,
                'property_type': object1.property_type.id,
                'location': object1.location.id,
            },
        )
        self.assert_status_code(200, response)
        assert len(response.data['results']) == 1, (
            f'Неверное количество объектов, должен быть 1 объект с '
            f'локацией {object1.location.id}.'
        )
        assert (
            response.data['results'][0]['id'] == object1.id
        ), f'Неверный объект. Должен быть объект с {object1.id}'
        response = client.get(
            url,
            {
                'property_type': object1.location.id,
                'rooms': object_rooms5.rooms,
            },
        )
        assert len(response.data['results']) == 1, (
            f'Неверное количество объектов, должен быть 1 объект с '
            f'локацией {object1.location.id} и количеством комнат '
            f'{object_rooms5.rooms}.'
        )

    def test_real_estate_filter_wrong_symbols(self, client, object1):
        """Test real estate filter with wrong symbols"""
        url = self.urls['real_estate_list']
        response = client.get(
            url,
            {
                'category': 'asd',
                'property_type': 'fgsg',
                'location': 'sdgerg',
                'rooms': 'sdfw'
            },
        )
        self.assert_status_code(200, response)
        assert len(response.data['results']) == 1, (
            'Неверное количество объектов, должен быть 1 объект'
        )
        # assert response.data['category'][0] == 'Введите число.'
        # assert response.data['property_type'][0] == 'Введите число.'
        # assert response.data['location'][0] == 'Введите число.'
        # assert response.data['rooms'][0] == 'Введите число.'