from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required

import MyMoney.forms as forms
import MyMoney.models as models

from Users.models import User, Group

from .algo import balance_transactions

from DjangoTools.decorators import(
    check_group,
)

@login_required
@check_group()
def show_balance(request, gid):
    group = Group.objects.get(id=gid)
    users_balance = {}
    group_users = models.User.objects.filter(groups__id = gid)
    for u in group_users:
        users_balance[str(u)] = 0
    group_expenses = models.Expense.objects.filter(group__id = gid)
    for exp in group_expenses:
        sum_shares = sum(exp.share_set.values_list("value", flat=True))
        for u in group_users:
            users_balance[str(u)] -= round((exp.share_set.get(owner=u).value/sum_shares)*exp.value,2)
        users_balance[str(exp.origin)] += exp.value
    transactions = balance_transactions(users_balance)
    return render(request, "balance.html", {
        "balance": users_balance,
        "group": group,
        "transactions": transactions})


@login_required
@check_group()
def add_expense(request, gid):
    if request.method == "GET":
        exp_form = forms.ExpenseForm()
        shares_fields = []
        for u in models.User.objects.filter(groups__id = gid):
            shares_fields.append(forms.ShareForm(initial={"owner": u}))
        return render(request, "expense.html", {
            "exp": exp_form,
            "shs": shares_fields})

    elif request.method == "POST":
        pass
