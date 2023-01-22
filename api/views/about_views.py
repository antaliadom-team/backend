from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

from about.models import StaticPage, Team
from api.serializers.about_serializers import (
    StaticPageSerializer,
    TeamSerializer,
)


class StaticPageViewSet(viewsets.ViewSet):
    """Получение и вывод статических страниц."""

    def list(self, request):
        queryset = StaticPage.objects.all()
        serializer = StaticPageSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = StaticPage.objects.all()
        page = get_object_or_404(queryset, pk=pk)
        serializer = StaticPageSerializer(page)
        return Response(serializer.data)


class TeamViewSet(viewsets.ViewSet):
    """Получение и вывод команды."""

    def list(self, request):
        queryset = Team.objects.all()
        serializer = TeamSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Team.objects.all()
        page = get_object_or_404(queryset, pk=pk)
        serializer = TeamSerializer(page)
        return Response(serializer.data)
