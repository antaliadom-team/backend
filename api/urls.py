from django.urls import include, path
from rest_framework import routers

from api.views.user_views import UserViewSet
from api.views.catalog_views import order

app_name = 'api'

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')

auth = [path('auth/', include('djoser.urls.jwt'))]

urlpatterns = [
    path('', include(auth)),
    path('order/', order, name='order'),
    path('', include(router.urls)),
]
