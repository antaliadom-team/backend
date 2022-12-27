
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer, TokenSerializer
from users.models import CustomUser


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
def php(request):
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

