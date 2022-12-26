from rest_framework import serializers
from .models import Estate, Buy, Rent, Images


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ('__all__')


class EstateSerializer(serializers.ModelSerializer):
    img = ImagesSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000,
                                     allow_empty_file=False,
                                     use_url=False),
        write_only=True
    )

    class Meta:
        model = Estate
        fields = ('id', 'title', 'price', 'area', 'floor', 'year', 'desc',
                  'img', 'uploaded_images',)

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images')
        flat = Estate.objects.create(**validated_data)
        for image in uploaded_images:
            new_flat = Images.objects.create(flat=flat, image=image)
        return flat


class BuySerializer(serializers.ModelSerializer):
    class Meta:
        model = Buy
        fields = ('__all__')


class RentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rent
        fields = ('__all__')
