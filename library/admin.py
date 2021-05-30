from django.contrib import admin

from .models import *


@admin.register(UserStorage)
class UserStorageAdmin(admin.ModelAdmin):
    list_display = ['user', 'specific_storage']


@admin.register(GroupStorage)
class GroupStorageAdmin(admin.ModelAdmin):
    list_display = ['group', 'user_init_storage']


@admin.register(Paper)
class PaperAdmin(admin.ModelAdmin):
    list_filter = ['user', 'file']


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_filter = ['user', 'name']
