from django.urls import include, path
from rest_framework import routers

from api.views.about_views import StaticPageViewSet, TeamViewSet
from api.views.catalog_views import (
    CategoryViewSet,
    FacilityViewSet,
    LocationViewSet,
    PropertyTypeViewSet,
    order,
)
from api.views.user_views import UserViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('locations', LocationViewSet, basename='locations')
router.register('categories', CategoryViewSet, basename='categories')
router.register('types', PropertyTypeViewSet, basename='types')
router.register('facilities', FacilityViewSet, basename='facilities')
router.register('static_pages', StaticPageViewSet, basename='static_pages')
router.register('team', TeamViewSet, basename='team')

auth = [path('auth/', include('djoser.urls.jwt'))]

urlpatterns = [
    path('', include(auth)),
    path('order/', order, name='order'),
    path('', include(router.urls)),
]
