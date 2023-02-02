from django.urls import include, path
from rest_framework import routers

from api.views.about_views import StaticPageViewSet, TeamViewSet
from api.views.catalog_views import (
    CategoryViewSet,
    FacilityViewSet,
    LocationViewSet,
    PropertyTypeViewSet,
    RealEstateViewSet,
    order,
    real_estate_order,
)
from api.views.user_views import UserViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('objects/locations', LocationViewSet, basename='locations')
router.register('objects/categories', CategoryViewSet, basename='categories')
router.register('objects/types', PropertyTypeViewSet, basename='types')
router.register('objects/facilities', FacilityViewSet, basename='facilities')
router.register('objects', RealEstateViewSet, basename='real_estate')
router.register('static_pages/team', TeamViewSet, basename='team')
router.register('static_pages', StaticPageViewSet, basename='static_pages')

auth = [path('auth/', include('djoser.urls.jwt'))]

urlpatterns = [
    path('', include(auth)),
    path('objects/order/', order, name='order'),
    path(
        'objects/<int:id>/order/', real_estate_order, name='real_estate_order'
    ),
    path('', include(router.urls)),
]
