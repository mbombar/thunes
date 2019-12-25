from django.urls import path

from MyMoney import views

app_name = "MyMoney"

urlpatterns = [
    path("<gid>/balance/", views.show_balance, name="balance"),
    path("<gid>/expense/new/", views.new_expense, name="new-expense"),
    path("<gid>/expense/history/", views.index_expense, name="index-expense"),
    path("<gid>/repay/<user1>/<user2>", views.rembourser, name="rembourser"),
    path("<gid>/expense/favorite/", views.favorite_expense, name="favorite-expense"),
    path("<gid>/expense/favorite/new", views.new_favorite_expense, name="new-favorite-expense"),
]
