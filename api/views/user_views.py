from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from djoser.views import UserViewSet as DjoserViewSet

from ..serializers.user_serializers import MyDjoserSerializer, TokenSerializer

User = get_user_model()

class MyDjoserViewSet(DjoserViewSet):
    """Для пользователя."""
    serializer_class = MyDjoserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        """Создание пользователя. Дополнительно заполняет поле username."""
        data = {}
        print(request.data)
        for key, value in request.data.items():
            data[f'{key}'] = value
        data['username'] = request.data['email'].split('@')[0]
        print(data)
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


# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from rest_framework_simplejwt.views import TokenObtainPairView

@api_view(http_method_names=['POST', ])
def token(request):
    """Выдает токен авторизации."""
    
    # settings.ACCOUNT_USER_MODEL_USERNAME_FIELD = 'email'
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    user = get_object_or_404(User, **data)
    refresh = RefreshToken.for_user(user)
    return Response(
        {'access': str(refresh.access_token)}, status=status.HTTP_201_CREATED
    )


# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)

#         # Add custom claims
#         token['email'] = user.email
#         token['username'] = user.email.split('@')[0]
#         token['password'] = user.password

#         return token

# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer