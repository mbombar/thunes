from django.urls import path

from . import views

app_name = "Users"

urlpatterns = [
    path("users/", views.index_users, name='users'),
    path("groups/", views.index_groups, name='groups'),
    path("create/", views.create_user, name="create_user"),
    ]
