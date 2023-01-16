from django.contrib import admin, auth
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser

# User = auth.get_user_model()


@admin.register(CustomUser)
class AdminUser(admin.ModelAdmin):

    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
        'phone_number',
        'email',
        'password',
    )

# admin.site.register(CustomUser, AdminUser)


