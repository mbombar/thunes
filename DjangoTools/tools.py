from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered

class ListModelAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields]
        super().__init__(model, admin_site)

def autoregister(*app_list):
        """
        Automatically register all the models from a given list 
        of apps to the admin site
        """
        for app in app_list:
            for model in apps.get_app_config(app).get_models():
                try:
                    admin.site.register(model, ListModelAdmin)
                except AlreadyRegistered:
                    pass

