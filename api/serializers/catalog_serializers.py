from rest_framework import serializers
from catalog.models import RealEstate, Image, Order


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"


class EstateSerializer(serializers.ModelSerializer):
    img = ImagesSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(
            max_length=1000000, allow_empty_file=False, use_url=False
        ),
        write_only=True,
    )

    class Meta:
        model = RealEstate
        fields = (
            "id",
            "title",
            "price",
            "area",
            "floor",
            "construction_year",
            "description",
            "rooms",
            "currency",
            "description",
            "period",
            "location",
            "type",
            "owner",
            "facilities",
            "date_added",
            "status",
            "rent_or_sell",
            "img",
            "uploaded_images",
        )

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")
        flat = RealEstate.objects.create(**validated_data)
        for image in uploaded_images:
            new_flat = Image.objects.create(flat=flat, image=image)
        return flat


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'user', 'real_estate',
            'email', 'first_name',
            'last_name', 'phone_number',
            'location', 'rooms',
            'comment', 'agreement',
            'confirmation_code', 'confitmed'
        )
        model = Order