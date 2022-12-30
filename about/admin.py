from django.contrib import admin

from about.models import StaticPage, Team


@admin.register(StaticPage)
class StaticPageAdmin(admin.ModelAdmin):
    """Админка статичных страниц."""

    list_display = ('title', 'slug', 'is_active')
    list_display_links = ('title',)
    search_fields = ('title', 'slug', 'content')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('is_active',)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Админка локации."""

    list_display = ('first_name', 'last_name', 'position', 'phone')
    list_display_links = ('first_name', 'last_name')
    search_fields = ('first_name', 'last_name', 'position', 'phone')
    list_filter = ('position', 'is_active')
    readonly_fields = ('date_added',)