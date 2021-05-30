from django.apps import AppConfig
from django.db.models.signals import post_migrate


class AdminSiteControllerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'admin_site_controller'
