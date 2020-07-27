from django.apps import AppConfig
from django.db.models.signals import post_save, post_delete


class MymoneyConfig(AppConfig):
    name = 'MyMoney'

    def ready(self):
        from . import signals

        post_save.connect(signals.invalidate_cache_on_update)
        post_delete.connect(signals.invalidate_cache_on_update)
