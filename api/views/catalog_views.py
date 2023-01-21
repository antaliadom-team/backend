from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from api.serializers.catalog_serializers import OrderSerializer

User = get_user_model()


@api_view(http_method_names=['POST'])
def order(request):
    # if request.user.is_active:
    serializer = OrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
