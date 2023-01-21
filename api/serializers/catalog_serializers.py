from rest_framework import serializers

from catalog.models import Order


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
