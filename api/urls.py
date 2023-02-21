from django.urls import include, path
from rest_framework import permissions, routers

from api.mixins import StaffBrowsableAPIMixin
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
from api.views.user_views import UserViewSet, logout

app_name = 'api'


class CustomAPIRootView(StaffBrowsableAPIMixin, routers.APIRootView):
    permission_classes = (permissions.IsAdminUser,)


class CustomDefaultRouter(routers.DefaultRouter):
    APIRootView = CustomAPIRootView


router = CustomDefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('objects/locations', LocationViewSet, basename='locations')
router.register('objects/categories', CategoryViewSet, basename='categories')
router.register(
    'objects/property_types', PropertyTypeViewSet, basename='property_types'
)
router.register('objects/facilities', FacilityViewSet, basename='facilities')
router.register('objects', RealEstateViewSet, basename='real_estate')
router.register('static_pages/team', TeamViewSet, basename='team')
router.register('static_pages', StaticPageViewSet, basename='static_pages')

auth = [path('auth/', include('djoser.urls.jwt'))]

urlpatterns = [
    path('', include(auth)),
    path(r'objects/order/', order, name='order'),
    path(
        r'objects/<int:object_id>/order/',
        real_estate_order,
        name='real_estate_order',
    ),
    path(r'users/logout/', logout, name='logout'),
    path('', include(router.urls)),
]
