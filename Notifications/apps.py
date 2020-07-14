from django.apps import AppConfig
from django.db.models.signals import post_save

class NotificationsConfig(AppConfig):
    name = 'Notifications'

    def ready(self):
        from MyMoney.models import Expense
        from . import signals

        post_save.connect(signals.discord_notification,
                          sender=Expense,
                          dispatch_uid="discord_notifications")
