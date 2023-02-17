from django.conf import settings
from django_filters import rest_framework as filters

from catalog.models import RealEstate


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    """Фильтр для поиска по списку значений. Значения разделяются запятыми"""
    # Например: ?locaiton=1,2,3


class RealEstateFilter(filters.FilterSet):
    """Фильтр недвижимости."""

    category = CharFilterInFilter(field_name='category__id', lookup_expr='in')
    property_type = CharFilterInFilter(
        field_name='property_type__id', lookup_expr='in'
    )
    location = CharFilterInFilter(field_name='location__id', lookup_expr='in')
    rooms = filters.NumberFilter(method='rooms_limiter')
    is_favorited = filters.BooleanFilter(method='get_favorite')

    class Meta:
        model = RealEstate
        fields = [
            'category',
            'property_type',
            'location',
            'rooms',
            'is_favorited',
        ]

    def get_favorite(self, queryset, name, value):
        """Возвращает избранные объекты недвижимости."""
        if value and self.request.user.is_authenticated:
            return queryset.filter(
                id__in=self.request.user.favorites.all()
                .values_list('real_estate_id', flat=True)
                .order_by('-date_added')
            )
        return queryset

    def rooms_limiter(self, queryset, name, value):
        """Возвращает объекты недвижимости с количеством комнат"""
        try:
            value = int(value)
        except ValueError:
            return queryset
        if 0 < value < settings.ROOMS_LIMIT:
            return queryset.filter(rooms=value).distinct()
        return queryset.filter(rooms__gte=settings.ROOMS_LIMIT).distinct()
