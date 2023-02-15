from django.contrib.auth import get_user_model

import pytest

from tests.common import APITestBase

User = get_user_model()


@pytest.mark.django_db(transaction=True)
class TestUserAPI(APITestBase):
    """Test user API"""

    def test_create_user_with_short_password(self, client):
        """Test create user with short password"""
        response = client.post(
            self.urls['users'],
            data={
                'email': 'test@fake.mail',
                'first_name': 'test',
                'last_name': 'lastnametest',
                'phone': '+79999999999',
                'password': '122q%5',
                're_password': '122q%5',
                'agreement': True,
            },
        )
        self.assert_status_code(400, response)
        assert response.data['password']['non_field_errors'][0] == (
            'Введённый пароль слишком короткий. '
            'Он должен содержать как минимум 7 символов.'
        ), 'Ошибка в создании пользователя с слишком коротким паролем'

    def test_create_user_with_password(self, client):
        """Test create user with password and all data"""
        User.objects.all().delete()
        data = {
            'email': 'test@fake.mail',
            'first_name': 'test',
            'last_name': 'lastnametest',
            'phone': '+79999999999',
            'password': '123$5Qq',
            're_password': '123$5Qq',
            'agreement': True,
        }
        response = client.post(self.urls['users'], data=data)
        self.assert_status_code(201, response)
        assert User.objects.count() == 1, 'Пользователь не создан'
        assert User.objects.first().email == data['email'], 'Неверный email'
        assert (
            User.objects.first().first_name == data['first_name']
        ), 'Неверное имя'
        assert (
            User.objects.first().last_name == data['last_name']
        ), 'Неверная фамилия'
        assert User.objects.first().phone == data['phone'], 'Неверный телефон'
        assert User.objects.first().check_password(
            data['password']
        ), 'Неверный пароль'
        assert (
            User.objects.first().agreement == data['agreement']
        ), 'Неверное соглашение, должно быть True'

    def test_create_user_without_email(self, client):
        """Test creating user with empty email"""
        response = client.post(
            self.urls['users'],
            data={
                'email': '',
                'first_name': 'test',
                'last_name': 'lastnametest',
                'phone': '+79999999999',
                'password': '122q%5',
                're_password': '122q%5',
                'agreement': True,
            },
        )
        self.assert_status_code(400, response)

    def test_create_user_without_agreement(self, client):
        """Test creating user without agreement"""
        response = client.post(
            self.urls['users'],
            data={
                'email': 'test@fake.mail',
                'first_name': 'test',
                'last_name': 'lastnametest',
                'phone': '+79999999999',
                'password': '122q%5',
                're_password': '122q%5',
            },
        )
        self.assert_status_code(400, response)
        assert response.data['agreement'][0] == (
            'Вы должны принять соглашение о конфиденциальности.'
        ), 'Ошибка в создании пользователя без соглашения о конфиденциальности'

    def test_create_user_with_different_passwords(self, client):
        """Test create user with different passwords"""
        response = client.post(
            self.urls['users'],
            data={
                'email': 'test@fake.mail',
                'first_name': 'test',
                'last_name': 'lastnametest',
                'phone': '+79999999999',
                'password': '122QQqq33%^',
                're_password': '0000erWERWER',
                'agreement': True,
            },
        )
        self.assert_status_code(400, response)
        assert response.data['password_error'][0] == (
            'Повторный пароль не совпадает с оригинальным.'
        ), 'Ошибка в создании пользователя с разными паролями'

    def test_create_user_with_wrong_name(self, client):
        """Test create user with wrong firstname"""
        response = client.post(
            self.urls['users'],
            data={
                'email': 'test@fake.mail',
                'first_name': 'test1111',
                'last_name': 'lastnametest111',
                'phone': '+79999999999',
                'password': '122QQqq33%^',
                're_password': '0000erWERWER',
                'agreement': True,
            },
        )
        self.assert_status_code(400, response)
        assert (
            response.data['first_name'][0]
            == 'Имя и Фамилия должны состоять только из букв и символа -.'
        ), 'Ошибка в создании пользователя с неверным именем'
        assert (
            response.data['last_name'][0]
            == 'Имя и Фамилия должны состоять только из букв и символа -.'
        ), 'Ошибка в создании пользователя с неверным именем'

    def test_usermanager_create_user_without_email(self):
        """Test User manager create user"""
        User.objects.all().delete()
        with pytest.raises(ValueError):
            User.objects.create_user(
                first_name='test',
                last_name='test',
                phone='+79999999999',
                password='123$5Qq',
            )
        assert (
            User.objects.count() == 0
        ), 'Пользователь создан, хотя не должен был'

    def test_usermanager_create_superuser(self):
        """Test User manager create superuser"""
        user = User.objects.create_superuser(
            email='admin@fake.mail',
            first_name='test',
            last_name='test',
            phone='+79999999999',
            password='123$5Qq',
        )
        assert user.is_superuser, 'Пользователь не является суперпользователем'

    def test_usermanager_create_superuser_without_is_superuser(self):
        """Test User manager create superuser with is_superuser=False"""
        User.objects.all().delete()
        with pytest.raises(ValueError):
            User.objects.create_superuser(
                email='admin@fake.mail',
                first_name='test',
                last_name='test',
                phone='+79999999999',
                password='123$5Qq',
                is_superuser=False,
            )
        assert (
            User.objects.count() == 0
        ), 'Пользователь создан, хотя не должен был'

    def test_usermanager_create_superuser_without_is_staff(self):
        """Test User manager create superuser with is_staff=False"""
        User.objects.all().delete()
        with pytest.raises(ValueError):
            User.objects.create_superuser(
                email='admin@fake.mail',
                first_name='test',
                last_name='test',
                phone='+79999999999',
                password='123$5Qq',
                is_staff=False,
            )

        assert (
            User.objects.count() == 0
        ), 'Пользователь создан, хотя не должен был'

    def test_delete_user(self, user_client, user):
        """Test forbidden method destroy for user's endpoint"""
        url = self.urls['users_detail'].format(user_id=user.id)
        self.assert_status_code(405, user_client.delete(url), url=url)

    def test_logout_user(self, user_client, token_user):
        """Test logout user"""
        url = self.urls['users_logout']
        self.assert_status_code(
            204,
            user_client.post(
                url, data={'refresh_token': token_user.get('refresh')}
            ),
            url=url,
        )
        self.assert_status_code(
            400,
            user_client.post(url, data={'refresh_token': 'wrong_token'}),
            url=url,
        )
