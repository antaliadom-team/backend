from django.conf import settings
from rest_framework import fields, serializers

from api.validators import regex_check_number, validate_name
from catalog.models import (
    Category,
    Facility,
    Image,
    Location,
    Order,
    OrderCategory,
    OrderLocation,
    OrderPropertyType,
    PropertyType,
    RealEstate,
)


class CommonOrderSerializer(serializers.ModelSerializer):
    """Общий сериализатор для заявок"""

    first_name = serializers.CharField(
        required=True,
        validators=(validate_name,),
        max_length=settings.NAMES_LENGTH,
    )
    last_name = serializers.CharField(
        required=True,
        validators=(validate_name,),
        max_length=settings.NAMES_LENGTH,
    )
    phone = serializers.CharField(
        required=True, validators=(regex_check_number,)
    )
    email = serializers.EmailField(
        required=True, max_length=settings.EMAIL_LENGTH
    )
    agreement = serializers.BooleanField(required=True)
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
    category = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all()
    )
    location = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Location.objects.all()
    )
    property_type = serializers.PrimaryKeyRelatedField(
        many=True, queryset=PropertyType.objects.all()
    )
    rooms = serializers.CharField()

    class Meta(CommonOrderSerializer.Meta):
        fields = CommonOrderSerializer.Meta.fields + (
            'category',
            'location',
            'property_type',
            'rooms',
        )

    def to_internal_value(self, data):
        data['rooms'] = ', '.join([str(i) for i in data['rooms']])
        return super().to_internal_value(data)

    def bulk_create_for_order_category(self, categories, order):
        """Создает несколько связей Тегов с Рецептом."""
        if categories:
            categories_objs = [
                OrderCategory(
                    category=category, order=order
                ) for category in categories
            ]
            OrderCategory.objects.bulk_create(
                objs=categories_objs,
                batch_size=len(categories_objs)
            )

    def bulk_create_for_order_location(self, locations, order):
        """Создает несколько связей Тегов с Рецептом."""
        if locations:
            location_objs = [
                OrderLocation(
                    location=location, order=order
                ) for location in locations
            ]
            OrderLocation.objects.bulk_create(
                objs=location_objs,
                batch_size=len(location_objs)
            )

    def bulk_create_for_order_property_type(self, property_types, order):
        """Создает несколько связей Тегов с Рецептом."""
        if property_types:
            property_type_objs = [
                OrderPropertyType(
                    property_type=property_type, order=order
                ) for property_type in property_types
            ]
            OrderPropertyType.objects.bulk_create(
                objs=property_type_objs,
                batch_size=len(property_type_objs)
            )

    def create(self, validated_data):
        categories = validated_data.pop('category')
        locations = validated_data.pop('location')
        property_types = validated_data.pop('property_type')
        order = Order.objects.create(**validated_data)
        self.bulk_create_for_order_category(categories=categories, order=order)
        self.bulk_create_for_order_location(locations=locations, order=order)
        self.bulk_create_for_order_property_type(
            property_types=property_types, order=order
        )
        return order


class RealEstateOrderSerializer(OrderSerializer):
    category = fields.ReadOnlyField(source='real_estate.category')

    class Meta(OrderSerializer.Meta):
        fields = OrderSerializer.Meta.fields


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
        """Дает избранное."""
        user = self.context['request'].user
        # Проверка на is_authenticated, иначе для анонимов
        # будет ошибка
        return (
            user.is_authenticated
            and user.favorites.filter(real_estate=obj).exists()
        )
