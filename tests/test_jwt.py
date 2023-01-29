import pytest

from tests.common import APITestBase


@pytest.mark.django_db(transaction=True)
class TestJWT(APITestBase):
    """Test JWT-Token API endpoints"""

    def test_get_token(self, user, user_client):
        """Test get token"""

        response = user_client.post(
            self.urls['get_token'],
            data={'email': user.email, 'password': '12345Qq'},
        )
        self.assert_status_code(200, response)
        assert response.data['access'] is not None, 'Ошибка в получении токена'

    def test_get_token_wrong_password(self, user, user_client):
        """Test get token with wrong password"""
        response = user_client.post(
            self.urls['get_token'],
            data={'email': user.email, 'password': 'wrong_password'},
        )
        self.assert_status_code(401, response)
        assert (
            response.data['detail']
            == 'No active account found with the given credentials'
        ), 'Ошибка в получении токена с неверным паролем'

    def test_get_token_wrong_email(self, user, user_client):
        """Test get token with wrong email"""
        response = user_client.post(
            self.urls['get_token'],
            data={'email': 'wrong_username@fake.mail', 'password': '12345Qq'},
        )
        self.assert_status_code(401, response)
        assert response.data['detail'] == (
            'No active account found with the given credentials'
        ), 'Ошибка в получении токена с неверным емейлом пользователя'

    def test_get_token_wrong_email_and_password(self, user_client):
        """Test get token with wrong email and password"""
        response = user_client.post(
            self.urls['get_token'],
            data={
                'email': 'wrong_username@fake.mail',
                'password': 'wrong_password',
            },
        )
        self.assert_status_code(401, response)
        assert response.data['detail'] == (
            'No active account found with the given credentials'
        ), 'Ошибка в получении токена с неверным емейлом пользователя'

    def test_get_token_without_username(self, user_client):
        """Test get token without email"""
        response = user_client.post(
            self.urls['get_token'], data={'password': '12345Qq'}
        )
        self.assert_status_code(400, response)
        assert response.data['email'][0] == (
            'Обязательное поле.'
        ), 'Ошибка в получении токена без имени пользователя'

    def test_get_token_without_password(self, user, user_client):
        """Test get token without password"""
        response = user_client.post(
            self.urls['get_token'], data={'email': user.email}
        )
        self.assert_status_code(400, response)
        assert response.data['password'][0] == (
            'Обязательное поле.'
        ), 'Ошибка в получении токена без пароля'

    def test_jwt_verify__valid_request_data(self, client, user):
        url = self.urls['verify_token']
        valid_data = {'email': user.email, 'password': '12345Qq'}
        response = client.post(self.urls['get_token'], data=valid_data)
        token_access = response.json().get('access')
        token_refresh = response.json().get('refresh')
        code_expected = 200
        response = client.post(url, data={'token': token_access})
        assert response.status_code == code_expected, (
            f'Убедитесь, что при запросе `{url}` с валидным параметром token, '
            f'возвращается код {code_expected}. '
            'Валидацию должны проходить как refresh, так и access токены'
        )
        response = client.post(url, data={'token': token_refresh})
        assert response.status_code == code_expected, (
            f'Убедитесь, что при запросе `{url}` с валидным параметром token, '
            f'возвращается код {code_expected}. '
            'Валидацию должны проходить как refresh, так и access токены'
        )

    def test_jwt_verify__invalid_request_data(self, client):
        url = self.urls['verify_token']

        response = client.post(url)
        code_expected = 400
        assert response.status_code == code_expected, (
            f'Убедитесь, что при запросе `{url}` без параметров, '
            f'возвращается код {code_expected}'
        )
        data_invalid = {'token': 'invalid token'}
        response = client.post(url, data=data_invalid)
        code_expected = 401
        assert response.status_code == code_expected, (
            f'Убедитесь, что при запросе `{url}` с невалидным значением '
            f'параметра token, возвращается код {code_expected}'
        )
        fields_expected = ['detail', 'code']
        for field in fields_expected:
            assert field in response.json(), (
                f'Убедитесь, что при запросе `{url}` с невалидным значением '
                f'параметра token, возвращается код {code_expected} с '
                f'соответствующим сообщением в поле {field}'
            )

    def test_jwt_refresh__valid_request_data(self, client, user):
        url = self.urls['refresh_token']
        valid_data = {'email': user.email, 'password': '12345Qq'}
        response = client.post(self.urls['get_token'], data=valid_data)
        token_refresh = response.json().get('refresh')
        code_expected = 200
        response = client.post(url, data={'refresh': token_refresh})
        assert response.status_code == code_expected, (
            f'Убедитесь, что при запросе `{url}` с валидным параметром '
            f'refresh, возвращается код {code_expected}'
        )
        field = 'access'
        assert field in response.json(), (
            f'Убедитесь, что при запросе `{url}` с валидным параметром '
            f'refresh, возвращается код {code_expected} и параметр access, '
            f'в котором передан новый токен'
        )

    def test_jwt_refresh__invalid_request_data(self, client):
        url = self.urls['refresh_token']

        response = client.post(url)
        code_expected = 400
        assert response.status_code == code_expected, (
            f'Убедитесь, что при запросе `{url}` без параметров, '
            f'возвращается код {code_expected}'
        )
        data_invalid = {'refresh': 'invalid token'}
        response = client.post(url, data=data_invalid)
        code_expected = 401
        assert response.status_code == code_expected, (
            f'Убедитесь, что при запросе `{url}` с невалидным значением '
            f'параметра refresh, возвращается код {code_expected}'
        )
        fields_expected = ['detail', 'code']
        for field in fields_expected:
            assert field in response.json(), (
                f'Убедитесь, что при запросе `{url}` с невалидным значением '
                f'параметра refresh, возвращается код {code_expected} с '
                f'соответствующим сообщением в поле {field}'
            )
