from djoser.views import UserViewSet as DjoserUsers
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


class UserViewSet(DjoserUsers):
    """Пользователи на основе Djoser."""

    http_method_names = ('get', 'post', 'put', 'patch', 'head')

    # Методы принудительно отключены для соответствия ТЗ

    def reset_username(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def set_username(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def reset_username_confirm(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(http_method_names=['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout(request):
    """Logout view."""
    try:
        RefreshToken(request.data['refresh']).blacklist()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception:
        return Response(status=status.HTTP_400_BAD_REQUEST)
