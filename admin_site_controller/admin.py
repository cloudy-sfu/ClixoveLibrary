from django.contrib import admin
# from django.contrib.admin.forms import AuthenticationForm
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

admin.site.site_url = "/main"
admin.site.site_header = admin.site.site_title = "Liboard"
admin.site.index_title = "Home"
# admin.site.has_permission = lambda request: request.user.is_active
# admin.site.login_form = AuthenticationForm


class RestrictedAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_user = request.user
        if obj.created_user == request.user or request.user.is_staff:
            obj.save()

    def delete_model(self, request, obj):
        if obj.created_user == request.user or request.user.is_staff:
            obj.delete()

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            if obj.created_user == request.user or request.user.is_staff:
                obj.delete()


@admin.register(ContentType)
class ContentTypeAdmin(admin.ModelAdmin):
    list_filter = ['app_label']


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'content_type', 'codename']
    list_filter = ['content_type']
