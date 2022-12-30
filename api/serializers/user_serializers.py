from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

# Нужно скопировать поле email в поле username  и возможно отрезать до собачки.

class MyDjoserSerializer(serializers.ModelSerializer):
    agreement = serializers.BooleanField()

    class Meta:
        write_only_fields = ('username',)
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
    
    # def validated_data(self, data):
    #     print(data)
    #     return data
    
    # def create(self, validated_data):
    #     validated_data['username'] = validated_data['email']
    #     print(validated_data)
    #     return validated_data
    
    

