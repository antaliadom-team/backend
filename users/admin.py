from django.contrib import admin, auth

User = auth.get_user_model()


@admin.register(User)
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
