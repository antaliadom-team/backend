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
        if (
            hasattr(instance, 'category')
            and instance.get_category() is not None
        ):
            data['category'] = instance.get_category()
        if (
            hasattr(instance, 'location')
            and instance.get_location() is not None
        ):
            data['location'] = instance.get_location()
        if (
            hasattr(instance, 'property_type')
            and instance.get_property_type() is not None
        ):
            data['property_type'] = instance.get_property_type()
        if hasattr(instance, 'comment') and instance.comment is None:
            data['comment'] = ''
        return data


class OrderSerializer(CommonOrderSerializer):
    category = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=Category.objects.all()
    )
    location = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Location.objects.all()
    )
    property_type = serializers.PrimaryKeyRelatedField(
        many=True, queryset=PropertyType.objects.all()
    )
    rooms = serializers.ListSerializer(
        child=serializers.IntegerField(), required=False
    )

    class Meta(CommonOrderSerializer.Meta):
        fields = CommonOrderSerializer.Meta.fields + (
            'category',
            'location',
            'property_type',
            'rooms',
        )

    @staticmethod
    def validate_rooms(value):
        for room in value:
            if not isinstance(room, int):
                raise serializers.ValidationError(
                    'Все значения должны быть числами.'
                )
            if room > 4:
                raise serializers.ValidationError(
                    'Число комнат не может быть больше 4.'
                )
        return value

    @staticmethod
    def bulk_create_for_order(objects, order, field, model):
        """Создает м2м связи локаций, категорий и типов с Заявкой."""
        if objects:
            categories_objs = [
                model(**{field: item}, order=order) for item in objects
            ]
            model.objects.bulk_create(
                objs=categories_objs, batch_size=len(categories_objs)
            )

    def create(self, validated_data):
        category = validated_data.pop('category')
        locations = validated_data.pop('location')
        property_types = validated_data.pop('property_type')
        order = Order.objects.create(**validated_data)
        OrderCategory.objects.create(order=order, category=category)
        self.bulk_create_for_order(
            objects=locations,
            order=order,
            field='location',
            model=OrderLocation,
        )
        self.bulk_create_for_order(
            objects=property_types,
            order=order,
            field='property_type',
            model=OrderPropertyType,
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
    image_328x261 = serializers.SerializerMethodField()
    image_738x632 = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ('id', 'image', 'image_328x261', 'image_738x632')

    def get_image_common(self, obj, scale):
        host_name = self.context[
            'request'
        ].build_absolute_uri().split('/api')[0]
        image_name, image_farmat = obj.image.url.split('.')
        return f'{host_name}{image_name}_{scale}.{image_farmat}'

    def get_image_328x261(self, obj):
        return self.get_image_common(obj, '328x261')

    def get_image_738x632(self, obj):
        return self.get_image_common(obj, '738x632')


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
