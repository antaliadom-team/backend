from django.conf import settings
from django_filters import rest_framework as filters

from catalog.models import RealEstate


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    """Фильтр для поиска по списку значений."""


class RealEstateFilter(filters.FilterSet):
    """Фильтр недвижимости."""

    category = CharFilterInFilter(field_name='category__id', lookup_expr='in')
    property_type = CharFilterInFilter(
        field_name='property_type__id', lookup_expr='in'
    )
    location = CharFilterInFilter(field_name='location__id', lookup_expr='in')
    rooms = filters.NumberFilter(method='rooms_limiter')
    is_favorited = filters.BooleanFilter(method='get_favorite')

    def get_favorite(self, queryset, name, value):
        """Возвращает избранные объекты недвижимости."""
        if value and self.request.user.is_authenticated:
            return self.queryset.filter(
                id__in=self.request.user.favorites.all()
                .values_list('real_estate_id', flat=True)
                .order_by('-date_added')
            )
        return queryset

    def rooms_limiter(self, queryset, name, value):
        """Возвращает объекты недвижимости с количеством комнат"""
        if 0 < value < settings.ROOMS_LIMIT:
            return self.queryset.filter(rooms=value)
        return self.queryset.filter(rooms__gte=settings.ROOMS_LIMIT)

    class Meta:
        model = RealEstate
        fields = [
            'category',
            'property_type',
            'location',
            'rooms',
            'is_favorited',
        ]
