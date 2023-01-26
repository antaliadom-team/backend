from djoser.views import UserViewSet as DjoserUsers
from rest_framework import status
from rest_framework.response import Response


class UserViewSet(DjoserUsers):
    """Пользователи на основе Djoser."""

    http_method_names = ('get', 'post', 'put', 'patch', 'head')

    # Методы принудительно отключены для соответствия ТЗ
    #
    def reset_password(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def activation(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def resend_activation(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def reset_username(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def set_username(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def reset_password_confirm(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def reset_username_confirm(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)
