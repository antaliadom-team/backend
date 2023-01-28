import pytest
from django.contrib.auth import get_user_model


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        email='test.user@fake.mail',
        password='12345Qq',
    )


@pytest.fixture
def another_user(django_user_model):
    return django_user_model.objects.create_user(
        email='another.test.user@fake.mail',
        password='12345Qq',
    )


@pytest.fixture
def admin(django_user_model):
    return django_user_model.objects.create_user(
        email='test.admin@fake.mail',
        password='12345Qq',
        is_superuser=True,
    )


@pytest.fixture
def token_admin(admin):
    from rest_framework_simplejwt.tokens import RefreshToken

    refresh = RefreshToken.for_user(admin)

    return {'refresh': str(refresh), 'access': str(refresh.access_token)}


@pytest.fixture
def admin_client(token_admin):
    from rest_framework.test import APIClient

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token_admin["access"]}')
    return client


@pytest.fixture
def token_user(user):
    from rest_framework_simplejwt.tokens import RefreshToken

    refresh = RefreshToken.for_user(user)
    return {'refresh': str(refresh), 'access': str(refresh.access_token)}


@pytest.fixture
def user_client(token_user):
    from rest_framework.test import APIClient

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token_user["access"]}')
    return client


@pytest.fixture
def client():
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture(
    params=[
        pytest.param(1, id='user 1'),
        pytest.param(2, id='user 2'),
        pytest.param(3, id='user 3'),
    ]
)
def some_users(request):
    return [
        get_user_model().objects.create_user(
            username=f'test_user_{i}',
            email=f'test.user{i}@fake.mail',
            password='123456Qq',
        )
        for i in range(request.param)
    ]
