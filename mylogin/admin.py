from django.contrib import admin
from .models import Register
from django.contrib.auth.models import Permission, ContentType


class PermissionAdmin(admin.ModelAdmin):
    list_display = ('content_type', 'codename')
    list_filter = ('content_type',)


class ContentTypeAdmin(admin.ModelAdmin):
    list_filter = ('app_label',)


admin.site.register(Register)
admin.site.register(Permission, PermissionAdmin)
admin.site.register(ContentType, ContentTypeAdmin)
admin.site.site_url = "/home"
