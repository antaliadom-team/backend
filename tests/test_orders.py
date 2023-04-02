import pytest

from tests.common import APITestBase


@pytest.mark.django_db(transaction=True)
class TestOrders(APITestBase):
    """Test orders API endpoint"""

    def test_anonymous_common_order(
        self, mocker, client, location, category1, property_type_apartment
    ):
        """Test anonymous orders"""
        mock_send_order_emails = mocker.patch(
            'api.views.catalog_views.send_order_emails'
        )
        url = self.urls['order_general']
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'phone': '1234567890',
            'email': 'test@example.com',
            'location': [location.id],
            'category': [category1.id],
            'property_type': [property_type_apartment.id],
            'agreement': True,
            'comment': 'Test comment',
            'rooms': [1, 2, 3],
        }
        response = client.post(url, data=data)
        self.assert_status_code(201, response, url=url)
        # assert that send_order_emails was called with the correct arguments
        mock_send_order_emails.apply_async.assert_called_once_with(
            kwargs={'data': response.data, 'user_id': None}, countdown=5
        )

    def test_common_order_with_empty_fields(self, mocker, client, category1):
        """Test anonymous orders with empty location, category, type"""
        mocker.patch('api.views.catalog_views.send_order_emails')
        url = self.urls['order_general']
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'phone': '1234567890',
            'email': 'test@example.com',
            'location': [],
            'category': category1.id,
            'property_type': [],
            'agreement': True,
            'comment': 'Test comment',
            'rooms': [],
        }
        response = client.post(url, data=data)
        self.assert_status_code(201, response, url=url)

    def test_common_order_wrong_category(
        self, mocker, client, location, property_type_apartment
    ):
        """Test anonymous orders with empty rooms"""
        mocker.patch('api.views.catalog_views.send_order_emails')
        url = self.urls['order_general']
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'phone': '1234567890',
            'email': 'test@example.com',
            'location': [location.id],
            'category': [3],
            'property_type': [property_type_apartment.id],
            'agreement': True,
            'comment': 'Test comment',
            'rooms': [],
        }
        response = client.post(url, data=data)
        self.assert_status_code(400, response, url=url)

    def test_common_order_wrong_rooms_5(
        self, mocker, client, location, category1, property_type_apartment
    ):
        """Test anonymous orders with room more than 4"""
        mocker.patch('api.views.catalog_views.send_order_emails')
        url = self.urls['order_general']
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'phone': '1234567890',
            'email': 'test@example.com',
            'location': [location.id],
            'category': [category1.id],
            'property_type': [property_type_apartment.id],
            'agreement': True,
            'comment': 'Test comment',
            'rooms': [1, 2, 3, 5],
        }
        response = client.post(url, data=data)
        self.assert_status_code(400, response, url=url)

    def test_user_common_order(
        self,
        mocker,
        user,
        user_client,
        location,
        category1,
        property_type_apartment,
    ):
        """Test anonymous orders"""
        mocker.patch('api.views.catalog_views.send_order_emails')
        url = self.urls['order_general']
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'phone': '1234567890',
            'email': 'test@example.com',
            'location': [location.id],
            'category': [category1.id],
            'property_type': [property_type_apartment.id],
            'agreement': True,
            'comment': 'Test comment',
            'rooms': [1, 2, 3],
        }
        response = user_client.post(url, data=data)
        self.assert_status_code(201, response, url=url)
        assert response.data['first_name'] == user.first_name
        assert response.data['last_name'] == user.last_name
        assert response.data['phone'] == user.phone
        assert response.data['email'] == user.email
