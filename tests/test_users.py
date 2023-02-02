import pytest
from django.contrib.auth import get_user_model

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
                'first_name': 'test1',
                'last_name': 'lastnametest2',
                'phone': '+79999999999',
                'password': '122q%5',
                're_password': '122q%5',
                'agreement': True,
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
                'agreement': True,
            },
        )
        self.assert_status_code(201, response)

    def test_create_user_without_email(self, client):
        """Test creating user with empty email"""
        response = client.post(
            self.urls['users'],
            data={
                'email': '',
                'first_name': 'test1',
                'last_name': 'lastnametest2',
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
                'first_name': 'test1',
                'last_name': 'lastnametest2',
                'phone': '+79999999999',
                'password': '122q%5',
                're_password': '122q%5',
            },
        )
        self.assert_status_code(400, response)
        assert response.data['agreement'][0] == (
            'Вы должны принять соглашение о конфиденциальности.'
        ), 'Ошибка в создании пользователя без соглашения о конфиденциальности'

    def test_usermanager_create_user_without_email(self):
        """Test User manager create user"""
        User.objects.all().delete()
        with pytest.raises(ValueError):
            User.objects.create_user(
                first_name='test1',
                last_name='test2',
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
            first_name='test1',
            last_name='test2',
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
                first_name='test1',
                last_name='test2',
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
                first_name='test1',
                last_name='test2',
                phone='+79999999999',
                password='123$5Qq',
                is_staff=False,
            )

        assert (
            User.objects.count() == 0
        ), 'Пользователь создан, хотя не должен был'
