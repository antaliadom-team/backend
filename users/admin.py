from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser



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

admin.site.register(CustomUser, AdminUser)


