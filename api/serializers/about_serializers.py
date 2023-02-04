from rest_framework import serializers

from about.models import StaticPage, Team


class StaticPageListSerializer(serializers.ModelSerializer):
    """Сериализатор списка статических страниц."""

    class Meta:
        model = StaticPage
        fields = ['id', 'title', 'slug']


class StaticPageSerializer(StaticPageListSerializer):
    """Сериализатор статических страниц."""

    class Meta(StaticPageListSerializer.Meta):
        fields = StaticPageListSerializer.Meta.fields + ['content']


class TeamSerializer(serializers.ModelSerializer):
    """Сериализатор команды."""

    class Meta:
        model = Team
        fields = (
            'id',
            'first_name',
            'last_name',
            'position',
            'photo',
            'phone',
        )
