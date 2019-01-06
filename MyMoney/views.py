from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory, formset_factory

import MyMoney.forms as forms
import MyMoney.models as models

from Users.models import User, Group

from .algo import balance_transactions

from DjangoTools.decorators import(
    check_group,
)

from .forms import(
    ExpenseForm,
    ShareForm,
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
def new_expense(request, gid):
    group = Group.objects.get(id=gid)
    n = group.user_set.count()
    if n == 0:
        raise Exception
    expense_form = ExpenseForm(request.POST or None)
    if request.method == "GET":
        # On crée des parts à 0 pour tous les membres du groupe
        ShareFormSet = formset_factory(ShareForm, extra=0)
        initial_share = []
        for user in group.user_set.all():
            initial_share.append({'value': 0, 'owner': user})
        share_formset = ShareFormSet(initial=initial_share)

        return render(request, "expense.html", {
            "expense_form": expense_form,
            "share_formset": share_formset,
            "group": group,
            }
        )
    else:
        if expense_form.is_valid():
            expense = expense_form.save(commit=False)


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
