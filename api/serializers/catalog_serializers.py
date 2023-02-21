from rest_framework import fields, serializers

from api.validators import regex_check_number, validate_name
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

    first_name = serializers.CharField(
        required=True, validators=(validate_name,)
    )
    last_name = serializers.CharField(
        required=True, validators=(validate_name,)
    )
    phone = serializers.CharField(
        required=True, validators=(regex_check_number,)
    )
    email = serializers.EmailField(required=True)
    date_added = fields.DateTimeField(read_only=True, format='%d.%m.%Y %H:%M')

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

    def __init__(self, instance=None, data=None, **kwargs):
        if data and 'context' in kwargs:
            user = kwargs['context']['request'].user
            if user.is_authenticated:
                data['first_name'] = user.first_name
                data['last_name'] = user.last_name
                data['phone'] = user.phone
                data['email'] = user.email

        super().__init__(instance=instance, data=data, **kwargs)

    def validate(self, data):
        if data and 'request' not in self.context:
            return data
        user = self.context['request'].user
        if user.is_authenticated:
            if not data.get('first_name'):
                data['first_name'] = user.first_name
            if not data.get('last_name'):
                data['last_name'] = user.last_name
            if not data.get('phone'):
                data['phone'] = user.phone
            if not data.get('email'):
                data['email'] = user.email
        return data

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
