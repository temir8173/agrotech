from django.apps import AppConfig


class BaseFrontConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base_front'
