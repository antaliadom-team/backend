from django.conf import settings
from django.contrib import admin
from django.db import models

from catalog.models import (
    SELL_TYPES,
    Category,
    Facility,
    Favorite,
    Image,
    Location,
    Order,
    PropertyType,
    RealEstate,
)
from core.utils import AdminImageWidget


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Админка заявки."""

    list_display = (
        'pk',
        'get_rooms',
        'first_name',
        'last_name',
        'phone',
        'email',
        'date_added',
        'review_date',
        'is_reviewed',
    )
    fields = (
        'get_rooms',
        'get_location',
        'get_category',
        'get_property_type',
        ('first_name', 'last_name'),
        'phone',
        'email',
        'date_added',
        'review_date',
        'is_reviewed',
    )
    search_fields = ('phone', 'email', 'first_name', 'last_name')
    list_filter = ('is_reviewed', 'date_added', 'review_date')
    readonly_fields = (
        'get_rooms',
        'get_location',
        'get_category',
        'get_property_type',
        'first_name',
        'last_name',
        'phone',
        'email',
        'date_added',
    )

    @admin.display(description='Количество комнат')
    def get_rooms(self, obj):
        return obj.rooms

    @admin.display(description='Локация')
    def get_location(self, obj):
        return obj.location.name or 'Не указано'

    @admin.display(description='Категория')
    def get_category(self, obj):
        return obj.category.name or 'Не указано'

    @admin.display(description='Тип недвижимости')
    def get_property_type(self, obj):
        return obj.property_type.name or 'Не указано'


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """Админка локации."""

    list_display = ('pk', 'name')
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
    max_num = settings.IMAGE_LIMIT


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

    class Media:
        js = ('admin/js/admin_period_visibility.js',)

    @admin.display(description='Цена')
    def price_with_currency(self, obj):
        """Вывод цены с валютой (и периодом в случае аренды)."""
        if obj.category.name == SELL_TYPES[0][1]:
            return f'{obj.price}{obj.currency}'
        return f'{obj.price}{obj.currency} в {obj.period.lower()}'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Админка избранного."""

    list_display = ('real_estate', 'user')
    list_display_links = ('real_estate',)
    search_fields = ('real_estate__name', 'user__username')
