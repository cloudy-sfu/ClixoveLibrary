from django.contrib import admin
from .models import *


class UserStorageAdmin(admin.ModelAdmin):
    list_display = ('user', 'specific_storage')


class GroupStorageAdmin(admin.ModelAdmin):
    list_display = ('group', 'user_init_storage')


class PaperAdmin(admin.ModelAdmin):
    list_filter = ('project',)


admin.site.register(GroupStorage, GroupStorageAdmin)
admin.site.register(UserStorage, UserStorageAdmin)
admin.site.register(Label)
admin.site.register(Paper)
