from django.urls import path

from MyMoney import views

app_name = "MyMoney"

urlpatterns = [
#    path("group/<gid>/expense/new/", views.add_expense),
#    path("group/<gid>/expense/<eid>/show/", views.show_expense),
#    path("group/<gid>/expense/<eid>/edit/", views.edit_expense),
    path("group/<gid>/balance/", views.show_balance)
]
