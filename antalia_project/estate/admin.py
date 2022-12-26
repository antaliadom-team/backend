from django.contrib import admin
from .models import Images, Estate


# class ImagesLine(admin.TabularInline):
#     fk_name = 'flat'
#     model = Images
#
#
# @admin.register(Flat)
# class FlatAdmin(admin.ModelAdmin):
#     inlines = [ImagesLine, ]
admin.site.register(Estate)
admin.site.register(Images)