from django.urls import path

from MyMoney import views

app_name = "MyMoney"

urlpatterns = [
    path("<gid>/expense/add/", views.add_expense),
#    path("<gid>/expense/<eid>/show/", views.show_expense),
#    path("<gid>/expense/<eid>/edit/", views.edit_expense),
    path("<gid>/balance/", views.show_balance, name="balance"),
    path("<gid>/expense/new/", views.new_expense, name="new-expense"),
]
