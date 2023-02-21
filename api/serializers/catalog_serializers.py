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


class CommonOrderSerializer(serializers.ModelSerializer):
    """Общий сериализатор для заявок"""

    first_name = serializers.CharField(required=False, allow_null=True)
    last_name = serializers.CharField(required=False, allow_null=True)
    phone = serializers.CharField(required=False, allow_null=True)
    email = serializers.EmailField(required=False, allow_null=True)
    date_added = fields.DateTimeField(read_only=True, format='%d.%m.%Y %H:%M')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user = request.user
            self.fields['first_name'].default = user.first_name
            self.fields['last_name'].default = user.last_name
            self.fields['phone'].default = user.phone
            self.fields['email'].default = user.email

    class Meta:
        fields = (
            'first_name',
            'last_name',
            'phone',
            'email',
            'comment',
            'agreement',
            'date_added',
        )
        model = Order

    def validate_agreement(self, value):
        if not value:
            raise serializers.ValidationError('Вы должны принять соглашение.')
        return value

    def to_representation(self, instance):
        data = super().to_representation(instance=instance)
        if hasattr(instance, 'category') and instance.category is not None:
            data['category'] = instance.category.name
        if hasattr(instance, 'location') and instance.location is not None:
            data['location'] = instance.location.name
        if (
            hasattr(instance, 'property_type')
            and instance.property_type is not None
        ):
            data['property_type'] = instance.property_type.name
        return data


class OrderSerializer(CommonOrderSerializer):
    class Meta(CommonOrderSerializer.Meta):
        fields = CommonOrderSerializer.Meta.fields + (
            'category',
            'location',
            'property_type',
            'rooms',
        )


class RealEstateOrderSerializer(OrderSerializer):
    category = fields.ReadOnlyField(source='real_estate.category')

    class Meta(OrderSerializer.Meta):
        pass


class LocationSerializer(serializers.ModelSerializer):
    """Сериализатор локаций"""

    class Meta:
        model = Location
        fields = ('id', 'name', 'slug')
        lookup_field = 'id'


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий"""

    class Meta:
        model = Category
        fields = ('id', 'name')
        lookup_field = 'name'


class PropertyTypeSerializer(serializers.ModelSerializer):
    """Сериализатор типов недвижимости"""

    class Meta:
        model = PropertyType
        fields = ('id', 'name')
        lookup_field = 'name'


class FacilitySerializer(serializers.ModelSerializer):
    """Сериализатор удобств"""

    class Meta:
        model = Facility
        fields = ('id', 'name', 'icon')
        lookup_field = 'id'


class ImageSerializer(serializers.ModelSerializer):
    """Сериализатор изображений"""

    class Meta:
        model = Image
        fields = ('id', 'image')


class RealEstateSerializer(serializers.ModelSerializer):
    """Сериализатор недвижимости"""

    is_favorited = fields.SerializerMethodField(default=False)
    facilities = FacilitySerializer(source='facility', many=True)
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = RealEstate
        fields = (
            'id',
            'title',
            'price',
            'location',
            'category',
            'property_type',
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

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        # Проверка на is_authenticated, иначе для анонимов
        # будет ошибка
        return (
            user.is_authenticated
            and user.favorites.filter(real_estate=obj).exists()
        )
