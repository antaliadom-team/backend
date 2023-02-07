from django_filters import rest_framework as filters

from catalog.models import RealEstate


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class RealEstateFilter(filters.FilterSet):
    category = CharFilterInFilter(
        field_name='category__id', lookup_expr='in')
    property_type = CharFilterInFilter(
        field_name='property_type__id', lookup_expr='in')
    location = CharFilterInFilter(field_name='location__id', lookup_expr='in')
    rooms = filters.NumberFilter()
    is_favorited = filters.BooleanFilter(method='get_favorite')

    def get_favorite(self, queryset, name, value):
        if value:
            return self.queryset.filter(
                id__in=self.request.user.favorites.all().values_list(
                    'real_estate_id', flat=True).order_by('-date_added'))
        return queryset

    class Meta:
        model = RealEstate
        fields = [
            'category', 'property_type', 'location', 'rooms', 'is_favorited'
        ]
