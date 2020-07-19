from django.urls import path

from Notifications.views import CreateWebhook, DeleteWebhook

app_name = "Notifications"

urlpatterns = [
    path("<int:webhook_id>/delete/", DeleteWebhook.as_view(), name="delete"),
    path("new/", CreateWebhook.as_view(), name="create"),
]
