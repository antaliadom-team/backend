from django.urls import path, include
# from rest_framework.routers import DefaultRouter

from .views import token, create_user, php #, UserViewSet, 

# router = DefaultRouter()
# router.register(r'users', UserViewSet)

app_name = 'api'

urlpatterns = [
    # path('v1', include(router.urls)),
    path('v1/registration/', create_user, name='registration'),
    path('v1/php/', php, name='php'),
    path('v1/auth/token/', token, name='token')
]
