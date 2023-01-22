from rest_framework import fields, serializers

from catalog.models import (
    Category,
    Facility,
    Image,
    Location,
    Order,
    PropertyType,
    RealEstate,
)


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
        fields = ('name', 'icon')
        lookup_field = 'name'


class ImageSerializer(serializers.ModelSerializer):
    """Сериализатор изображений"""

    class Meta:
        model = Image
        fields = ('id', 'image')


class RealEstateSerializer(serializers.ModelSerializer):
    """Сериализатор недвижимости"""

    is_favorited = fields.SerializerMethodField(default=False)
    facilities = FacilitySerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        # Проверка на is_authenticated, иначе для анонимов
        # будет ошибка
        return (
            user.is_authenticated
            and user.favorites.filter(real_estate=obj).exists()
        )

    class Meta:
        model = RealEstate
        fields = (
            'title',
            'price',
            'location',
            'category',
            'type',
            'rooms',
            'area',
            'total_floors',
            'floor',
            'construction_year',
            'status',
            'currency',
            'period',
            'description',
            'facilities',
            'images',
            'is_favorited',
        )
