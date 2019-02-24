from django.urls import path

from . import views

app_name = "Users"

urlpatterns = [
    path("users/", views.index_users, name='users'),
    path("groups/", views.index_groups, name='groups'),
    path("create/", views.create_user, name="create_user"),
    path("groups/create/", views.create_edit_group, name="create_group"),
    path("groups/edit/<gid>/", views.create_edit_group, name="edit_group"),
    ]
