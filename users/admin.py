from django.contrib import admin, auth
from django.contrib.auth import admin as auth_admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

User = auth.get_user_model()


@admin.register(User)
class AdminUser(UserAdmin):
    """Админка для пользователей"""

    ordering = ('email',)
    search_fields = ('email', 'first_name', 'last_name', 'phone')
    list_display = ('email', 'first_name', 'last_name', 'phone', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            'Персональная информация',
            {'fields': ('first_name', 'last_name', 'phone')},
        ),
        (
            'Разрешения',
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                )
            },
        ),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )
    limited_fieldsets = (
        (None, {'fields': ('email',)}),
        (
            'Персональная информация',
            {'fields': ('first_name', 'last_name', 'phone')},
        ),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2'),
            },
        ),
    )
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = auth_admin.AdminPasswordChangeForm
