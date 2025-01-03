from django.apps import AppConfig


class AddAllConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'add_all'

    def ready(self):
        import .signals  # Signalni ulash
