from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views.user_views import MyDjoserViewSet
from api.views.catalog_views import order

router = DefaultRouter()
router.register(r'users', MyDjoserViewSet, basename='users')

app_name = 'api'

urlpatterns = [
    path('auth/', include(router.urls)),
    path('auth/', include('djoser.urls.jwt')),
    path('order/', order, name='order'),
]
