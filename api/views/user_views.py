from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from djoser.views import UserViewSet# as DjoserViewSet
from django.conf import settings

from api.serializers.user_serializers import MyDjoserSerializer

# from users.models import CustomUser as User

User = get_user_model()

class MyDjoserViewSet(UserViewSet):
    """Для пользователя."""
    queryset = User.objects.all()
    # def get_queryset(self):
    #     return User.objects.filter(id=self.request.user.id )


    def get_serializer(self, *args, **kwargs):
        serializer_class = MyDjoserSerializer
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        """Создание пользователя. Дополнительно заполняет поле username."""
        data = {}
        for key, value in request.data.items():
            data[f'{key}'] = value
        data['username'] = request.data['email']
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def reset_password(self, request, args, **kwargs):
        """Удаление эндпоинта."""
        return Response(status=status.HTTP_404_NOT_FOUND)

    def activation(self, request,args, kwargs):
        """Удаление эндпоинта."""
        return Response(status=status.HTTP_404_NOT_FOUND)

    def resend_activation(self, request, *args, kwargs):
        """Удаление эндпоинта."""
        return Response(status=status.HTTP_404_NOT_FOUND)

    def reset_username(self, request, args, **kwargs):
        """Удаление эндпоинта."""
        return Response(status=status.HTTP_404_NOT_FOUND)

    def set_username(self, request,args, kwargs):
        """Удаление эндпоинта."""
        return Response(status=status.HTTP_404_NOT_FOUND)

    def reset_password_confirm(self, request, *args, kwargs):
        """Удаление эндпоинта."""
        return Response(status=status.HTTP_404_NOT_FOUND)

    def reset_username_confirm(self, request, *args, **kwargs):
        """Удаление эндпоинта."""
        return Response(status=status.HTTP_404_NOT_FOUND)

