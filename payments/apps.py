# from django.apps import AppConfig


# class PaymentsConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'payments'

# from django.apps import AppConfig

# class PaymentsConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'payments'

#     # 🟢 ADDED — ensures signals are automatically loaded
#     def ready(self):
#         import payments.signals  # noqa

# payments/apps.py
from django.apps import AppConfig

class PaymentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payments'

    # CHANGED: ensure signals register when app is ready
    def ready(self):
        # import signals here so Django registers them when the app loads
        import payments.signals  # noqa: F401
