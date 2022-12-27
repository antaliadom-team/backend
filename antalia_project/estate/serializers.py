from rest_framework import serializers
from .models import Estate, Images


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
        fields = ('id', 'title', 'price', 'area', 'floor', 'construction_year',
                  'description', 'rooms', 'currency', 'description',
                  'period', 'location', 'type', 'owner', 'facilities',
                  'date_added', 'status', 'rent_or_sell', 'img', 'uploaded_images')

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images')
        flat = Estate.objects.create(**validated_data)
        for image in uploaded_images:
            new_flat = Images.objects.create(flat=flat, image=image)
        return flat

