from django.urls import path

from MyMoney import views

app_name = "MyMoney"

urlpatterns = [
    path("<gid>/balance/", views.show_balance, name="balance"),
    path("<gid>/expense/new/", views.new_expense, name="new-expense"),
    path("<gid>/expense/history/", views.index_expense, name="index-expense"),
]
