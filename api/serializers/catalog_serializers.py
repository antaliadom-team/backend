from rest_framework import serializers

from catalog.models import Category, Facility, Location, Order, PropertyType


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'user',
            'real_estate',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'location',
            'rooms',
            'comment',
            'agreement',
            'confirmation_code',
            'confirmed',
        )
        model = Order


class LocationSerializer(serializers.ModelSerializer):
    """Сериализатор локаций"""

    class Meta:
        model = Location
        fields = ('name', 'slug')
        lookup_field = 'slug'


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий"""

    class Meta:
        model = Category
        fields = ('name',)
        lookup_field = 'name'


class PropertyTypeSerializer(serializers.ModelSerializer):
    """Сериализатор типов недвижимости"""

    class Meta:
        model = PropertyType
        fields = ('name',)
        lookup_field = 'name'


class FacilitySerializer(serializers.ModelSerializer):
    """Сериализатор удобств"""

    class Meta:
        model = Facility
        fields = ('name',)
        lookup_field = 'name'
