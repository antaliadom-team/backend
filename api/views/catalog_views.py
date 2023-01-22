from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers.catalog_serializers import (
    CategorySerializer,
    FacilitySerializer,
    LocationSerializer,
    OrderSerializer,
    PropertyTypeSerializer,
)
from catalog.models import Category, Facility, Location, PropertyType

User = get_user_model()


@api_view(http_method_names=['POST'])
def order(request):
    serializer = OrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


class LocationViewSet(viewsets.ModelViewSet):
    """Локация"""

    http_method_names = ('get',)
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    lookup_field = 'slug'
    search_fields = ('name', 'slug')
    ordering = ('name',)


class CategoryViewSet(viewsets.ModelViewSet):
    """Категория"""

    http_method_names = ('get',)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'name'


class PropertyTypeViewSet(viewsets.ModelViewSet):
    """Тип недвижимости"""

    http_method_names = ('get',)
    queryset = PropertyType.objects.all()
    serializer_class = PropertyTypeSerializer
    lookup_field = 'name'


class FacilityViewSet(viewsets.ModelViewSet):
    """Удобства"""

    http_method_names = ('get',)
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer
    lookup_field = 'name'
