from django.contrib import admin
from django.db import models

from catalog.models import (
    Category,
    Facility,
    Favorite,
    Image,
    Location,
    PropertyType,
    RealEstate,
)
from core.utils import AdminImageWidget


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """Админка локации."""

    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    """Админка типа объекта."""

    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ('name',)


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    """Админка удобств."""

    list_display = ('name', 'icon')
    list_display_links = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'icon': ('name',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админка аренда/продажа."""

    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ('name',)


class ImageInline(admin.TabularInline):
    """Инлайн изображений."""

    formfield_overrides = {models.ImageField: {'widget': AdminImageWidget}}
    model = Image
    extra = 0
    # TODO: вынести в настройки, чтобы можно было менять
    max_num = 6  # Максимальное количество изображений


@admin.register(RealEstate)
class RealEstateAdmin(admin.ModelAdmin):
    """Админка объекта."""

    fields = (
        'title',
        'location',
        'category',
        ('price', 'currency', 'period'),
        'area',
        ('floor', 'total_floors'),
        'construction_year',
        'rooms',
        'status',
        'description',
        'property_type',
        'facility',
        'owner',
        'date_added',
    )
    list_display = (
        'title',
        'location',
        'category',
        'price_with_currency',
        'area',
        'rooms',
        'status',
        'property_type',
    )
    list_display_links = ('title',)
    search_fields = ('title', 'description')
    list_filter = ('status', 'location', 'property_type')  # 'owner'
    readonly_fields = ('date_added',)
    inlines = (ImageInline,)

    @admin.display(description='Цена')
    def price_with_currency(self, obj):
        """Вывод цены с валютой (и периодом в случае аренды)."""
        if obj.category.name == 'Продажа':
            return f'{obj.price}{obj.currency}'
        return f'{obj.price}{obj.currency} в {obj.period.lower()}'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Админка избранного."""

    list_display = ('real_estate', 'user')
    list_display_links = ('real_estate',)
    search_fields = ('real_estate__name', 'user__username')
