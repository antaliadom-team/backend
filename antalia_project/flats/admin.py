from django.contrib import admin
from .models import Images, Flat


# class ImagesLine(admin.TabularInline):
#     fk_name = 'flat'
#     model = Images
#
#
# @admin.register(Flat)
# class FlatAdmin(admin.ModelAdmin):
#     inlines = [ImagesLine, ]
admin.site.register(Flat)
admin.site.register(Images)