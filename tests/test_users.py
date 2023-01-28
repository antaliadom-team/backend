import pytest

from tests.common import APITestBase


@pytest.mark.django_db(transaction=True)
class TestUserAPI(APITestBase):
    """Test user API"""

    def test_create_user_with_short_password(self, client):
        """Test create user with short password"""
        response = client.post(
            self.urls['users'],
            data={
                'email': 'test@fake.mail',
                'first_name': 'test1',
                'last_name': 'lastnametest2',
                'phone': '+79999999999',
                'password': '122q%5',
                're_password': '122q%5',
            },
        )
        self.assert_status_code(400, response)
        assert response.data['password'][0] == (
            'Введённый пароль слишком короткий. '
            'Он должен содержать как минимум 7 символов.'
        ), 'Ошибка в создании пользователя с слишком коротким паролем'

    def test_create_user_with_password(self, client):
        """Test create user with password"""
        response = client.post(
            self.urls['users'],
            data={
                'email': 'test@fake.mail',
                'first_name': 'test1',
                'last_name': 'lastnametest2',
                'phone': '+79999999999',
                'password': '123$5Qq',
                're_password': '123$5Qq',
            },
        )
        self.assert_status_code(201, response)
