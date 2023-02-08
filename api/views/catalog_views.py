from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response

from api.mixins import FavoriteMixin
from api.pagination import ObjectsLimitPagePagination
from api.serializers.catalog_serializers import (
    CategorySerializer,
    FacilitySerializer,
    LocationSerializer,
    OrderSerializer,
    PropertyTypeSerializer,
    RealEstateOrderSerializer,
    RealEstateSerializer,
)
from catalog.filters import RealEstateFilter
from catalog.models import (
    Category,
    Facility,
    Favorite,
    Location,
    PropertyType,
    RealEstate,
)
from core.utils import send_order_emails

User = get_user_model()


@api_view(http_method_names=['POST'])
@permission_classes([permissions.AllowAny])
def order(request):
    """Заявка общая"""
    serializer = OrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    send_order_emails(serializer.data, user=request.user or None)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(http_method_names=['POST'])
def real_estate_order(request):
    """Заявка на конкретный объект недвижимости"""
    serializer = RealEstateOrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    send_order_emails(serializer.data, user=request.user or None)
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
    lookup_field = 'id'


class PropertyTypeViewSet(viewsets.ModelViewSet):
    """Тип недвижимости"""

    http_method_names = ('get',)
    queryset = PropertyType.objects.all()
    serializer_class = PropertyTypeSerializer
    lookup_field = 'id'


class FacilityViewSet(viewsets.ModelViewSet):
    """Удобства"""

    http_method_names = ('get',)
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer
    lookup_field = 'id'


class RealEstateViewSet(viewsets.ModelViewSet, FavoriteMixin):
    """Каталог недвижимости"""

    http_method_names = ('get', 'post', 'delete')
    queryset = RealEstate.objects.all()
    serializer_class = RealEstateSerializer
    pagination_class = ObjectsLimitPagePagination
    filter_backends = (DjangoFilterBackend, )
    filterset_class = RealEstateFilter

    @action(
        methods=('post', 'delete'),
        detail=True,
        permission_classes=(permissions.IsAuthenticated,),
    )
    def favorite(self, request, pk=None):
        # Добавление объекта в избранное
        if request.method == 'POST':
            return self.add_object(request, pk=pk, model=Favorite)
        # Удаление объекта из избранного
        return self.delete_object(request, pk=pk, model=Favorite)
