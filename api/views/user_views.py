from django.contrib.auth import get_user_model
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from djoser.views import UserViewSet as DjoserViewSet

from ..serializers.user_serializers import UserSerializer,TokenSerializer, MyDjoserSerializer
from users.models import CustomUser
# НУЖНО РАЗОБРАТЬСЯ С ТОКЕНАМИ,ОНИ ПОКА НЕ РАБОТАЮТ!!!!!!!!!!
User = get_user_model()


@api_view(http_method_names=['POST', ])
def create_user(request):
    """Creating user."""
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes(permission_classes=(IsAuthenticated,))
@api_view(http_method_names=['GET', 'PATCH'])
def profile(request):
    """Personal Home Page."""
    # users = CustomUser.objects.all()
    if request.method == 'PATCH':
        user = get_object_or_404(CustomUser, id=request.user.id)
        serializer = UserSerializer(user, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    serializer = UserSerializer(request.user, many=False)
    # serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(http_method_names=['POST', ])
def token(request):
    """Выдает токен авторизации."""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    user = get_object_or_404(CustomUser, **data)
    refresh = RefreshToken.for_user(user)
    return Response(
        {'access': str(refresh.access_token)}, status=status.HTTP_201_CREATED
    )

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



