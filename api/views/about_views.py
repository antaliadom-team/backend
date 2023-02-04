from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

from about.models import StaticPage, Team
from api.serializers.about_serializers import (
    StaticPageSerializer,
    TeamSerializer, StaticPageListSerializer,
)


class StaticPageViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение и вывод статических страниц."""

    queryset = StaticPage.objects.filter(is_active=True)
    serializer_class = StaticPageSerializer
    list_serializer_class = StaticPageListSerializer

    def list(self, request, *args, **kwargs):
        """Список статических страниц."""
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.list_serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """Получение статической страницы."""
        instance = get_object_or_404(StaticPage, pk=kwargs['pk'])
        serializer = self.serializer_class(instance)
        return Response(serializer.data)


class TeamViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение и вывод команды."""

    queryset = Team.objects.filter(is_active=True)

    def list(self, request, *args, **kwargs):
        """Список команды."""
        queryset = self.filter_queryset(self.get_queryset())
        serializer = TeamSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """Получение члена команды."""
        instance = get_object_or_404(Team, pk=kwargs['pk'])
        serializer = TeamSerializer(instance)
        return Response(serializer.data)
