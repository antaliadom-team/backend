from urllib.parse import urlparse

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response

from antalia_project.tasks import send_order_emails
from api.filters import RealEstateFilter
from api.metrics import save_metrics
from api.mixins import FavoriteMixin
from api.pagination import ObjectsLimitPagePagination
from api.serializers.catalog_serializers import (
    CategorySerializer,
    ConditionalRealEstateSerializer,
    FacilitySerializer,
    LocationSerializer,
    OrderSerializer,
    PropertyTypeSerializer,
    RealEstateOrderSerializer,
    RealEstateSerializer,
)
from catalog.models import (
    Category,
    Facility,
    Favorite,
    Location,
    PropertyType,
    RealEstate,
)

User = get_user_model()


@api_view(http_method_names=['POST'])
@permission_classes([permissions.AllowAny])
@save_metrics
def order(request):
    """Заявка общая"""
    serializer = OrderSerializer(
        data=request.data, context={'request': request}
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    send_order_emails.apply_async(
        kwargs={'data': serializer.data, 'user_id': request.user.id or None},
        countdown=5,
    )
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(http_method_names=['POST'])
@permission_classes([permissions.AllowAny])
@save_metrics
def real_estate_order(request, object_id=None):
    """Заявка на конкретный объект недвижимости"""
    real_estate = get_object_or_404(RealEstate, pk=object_id)
    serializer = RealEstateOrderSerializer(
        data=request.data, context={'request': request}
    )
    serializer.is_valid(raise_exception=True)
    serializer.save(
        real_estate=real_estate,
        # Lists as a universal solution for both types of orders
        # (common and real estate)
        rooms=[real_estate.rooms],
        category=[real_estate.category],
        property_type=[real_estate.property_type],
        location=[real_estate.location],
    )

    object_url = urlparse(request.build_absolute_uri())

    send_order_emails.apply_async(
        kwargs={
            'data': serializer.data,
            'user_id': request.user.id or None,
            'real_estate_id': real_estate.id,
            'object_url': (
                f'{object_url.scheme}://{object_url.netloc}/object/{real_estate.id}/',  # noqa
            ),
        },
        countdown=5,
    )
    return Response(serializer.data, status=status.HTTP_201_CREATED)


class LocationViewSet(viewsets.ModelViewSet):
    """Локация"""

    http_method_names = ('get',)
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    authentication_classes = []
    lookup_field = 'id'
    search_fields = ('name', 'slug')
    ordering = ('name',)


class CategoryViewSet(viewsets.ModelViewSet):
    """Категория"""

    http_method_names = ('get',)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = []
    lookup_field = 'id'


class PropertyTypeViewSet(viewsets.ModelViewSet):
    """Тип недвижимости"""

    http_method_names = ('get',)
    queryset = PropertyType.objects.all()
    serializer_class = PropertyTypeSerializer
    authentication_classes = []
    lookup_field = 'id'


class FacilityViewSet(viewsets.ModelViewSet):
    """Удобства"""

    http_method_names = ('get',)
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer
    authentication_classes = []
    lookup_field = 'id'


class RealEstateViewSet(viewsets.ModelViewSet, FavoriteMixin):
    """Каталог недвижимости"""

    http_method_names = ('get', 'post', 'delete')
    queryset = RealEstate.objects.all()
    serializer_class = RealEstateSerializer
    pagination_class = ObjectsLimitPagePagination
    filter_backends = (DjangoFilterBackend,)
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

    def get_serializer_class(self):
        # Использование кастомного сериализатора для модели 'RealEstate'
        # при действиях 'list' и 'retrieve'
        if self.action in ('list', 'retrieve'):
            return ConditionalRealEstateSerializer
        return RealEstateSerializer
