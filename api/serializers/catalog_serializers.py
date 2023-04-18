from django.conf import settings
from django.core import validators
from rest_framework import fields, serializers

from api.validators import regex_check_number, validate_name
from catalog.models import (
    SELL_TYPES,
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

    @staticmethod
    def validate_agreement(value):
        if not value:
            raise serializers.ValidationError('Вы должны принять соглашение.')
        return value

    def to_representation(self, instance):
        data = super().to_representation(instance=instance)
        user = self.context['request'].user
        if user.is_authenticated:
            data['first_name'] = user.first_name
            data['last_name'] = user.last_name
            data['phone'] = user.phone
            data['email'] = user.email
        if isinstance(instance, RealEstate):
            return data
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
        if hasattr(instance, 'rooms') and instance.rooms is not None:
            data['rooms'] = instance.get_rooms()
        else:
            data['rooms'] = ''
        return data


class OrderSerializer(CommonOrderSerializer):
    category = serializers.PrimaryKeyRelatedField(
        many=False, queryset=Category.objects.all(), required=False
    )
    location = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Location.objects.all(), required=False
    )
    property_type = serializers.PrimaryKeyRelatedField(
        many=True, queryset=PropertyType.objects.all(), required=False
    )
    rooms = serializers.ListField(
        child=serializers.IntegerField(
            validators=[
                validators.MinValueValidator(1),
                validators.MaxValueValidator(4),
            ]
        ),
        required=False,
    )

    class Meta(CommonOrderSerializer.Meta):
        fields = CommonOrderSerializer.Meta.fields + (
            'category',
            'location',
            'property_type',
            'rooms',
        )

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
        category = None
        locations = None
        property_types = None
        if 'category' in validated_data:
            category = validated_data.pop('category')
        if 'location' in validated_data:
            locations = validated_data.pop('location')
        if 'property_type' in validated_data:
            property_types = validated_data.pop('property_type')
        order = Order.objects.create(**validated_data)
        if category:
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


class RealEstateOrderSerializer(CommonOrderSerializer):
    category = fields.ReadOnlyField(source='real_estate.category')
    location = fields.ReadOnlyField(source='real_estate.location')
    property_type = fields.ReadOnlyField(source='real_estate.property_type')

    class Meta(OrderSerializer.Meta):
        fields = OrderSerializer.Meta.fields + (
            'category',
            'location',
            'property_type',
        )


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

    image_thumbnails = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ('id', 'image', 'image_thumbnails')

    def get_image_thumbnails(self, obj):
        sizes = getattr(settings, 'PREVIEW_SIZES', None)
        if not sizes:
            return {}
        urls = {}
        for size in sizes:
            filename = obj.filename_generator(obj.image.name, size)
            urls[f'{size[0]}x{size[1]}'] = self.context.get(
                'request'
            ).build_absolute_uri(f'{settings.MEDIA_URL}{filename}')
        return urls


class RealEstateSerializer(serializers.ModelSerializer):
    """Сериализатор объекта недвижимости"""

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


class ConditionalRealEstateSerializer(RealEstateSerializer):
    """Сериализатор недвижимости с условием вывода поля 'period'"""

    def to_representation(self, instance):
        # Вызываем метод родительского класса для получения данных
        # сериализатора
        data = super().to_representation(instance)
        # Удаляем поле 'period' если категория 'Аренда'
        if instance.category.name == SELL_TYPES[0][1]:
            data.pop('period', None)
        return data
