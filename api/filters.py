from django.conf import settings
from django_filters import rest_framework as filters

from catalog.models import RealEstate


class RealEstateFilter(filters.FilterSet):
    """Фильтр недвижимости."""

    category = filters.BaseInFilter(field_name='category__id', lookup_expr='in')
    property_type = filters.BaseInFilter(
        field_name='property_type__id', lookup_expr='in'
    )
    location = filters.BaseInFilter(field_name='location__id', lookup_expr='in')
    rooms = filters.Filter(method='rooms_limiter')
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

    def filter_queryset(self, queryset):
        """Возвращает оригинальный кверисет в случае ошибки ValueError"""
        try:
            return super().filter_queryset(queryset)
        except ValueError:
            return queryset

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
