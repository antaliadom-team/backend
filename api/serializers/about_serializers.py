from rest_framework import serializers

from about.models import StaticPage, Team


class StaticPageSerializer(serializers.ModelSerializer):
    """Сериализатор статических страниц."""

    class Meta:
        model = StaticPage
        fields = '__all__'


class TeamSerializer(serializers.ModelSerializer):
    """Сериализатор команды."""

    class Meta:
        model = Team
        fields = '__all__'
