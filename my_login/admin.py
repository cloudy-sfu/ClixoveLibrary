from django.contrib import admin
from django.contrib.auth import authenticate

from .models import *


@admin.register(Register)
class RegisterAdmin(admin.ModelAdmin):
    list_display = ['group', 'username', 'bio']
    list_filter = ['group']
    actions = ['admit']
    exclude = ['password']
    search_fields = ['bio']

    def admit(self, _, queryset):
        for application in queryset:
            new_user, created = User.objects.get_or_create(username=application.username)
            if created:
                new_user.set_password(application.password)
                new_user.save()
            else:
                new_user = authenticate(username=application.username, password=application.password)
                if not new_user:
                    application.delete()
                    continue
            new_user.groups.add(application.group)
            application.delete()

    admit.short_description = "Admit"
