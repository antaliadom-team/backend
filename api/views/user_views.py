from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from djoser.views import UserViewSet as DjoserViewSet

from ..serializers.user_serializers import MyDjoserSerializer

User = get_user_model()

class MyDjoserViewSet(DjoserViewSet):
    serializer_class = MyDjoserSerializer
    queryset = User.objects.all()

    def reset_password(self, request, args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def activation(self, request,args, kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def resend_activation(self, request, *args, kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def reset_username(self, request, args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def set_username(self, request,args, kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def reset_password_confirm(self, request, *args, kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def reset_username_confirm(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)
