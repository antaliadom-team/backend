from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class MyDjoserSerializer(serializers.ModelSerializer):
    agreement = serializers.BooleanField()

    class Meta:
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'password',
            'agreement',
            'role',
        )
        model = User
