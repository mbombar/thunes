from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required

import MyMoney.forms as forms
import MyMoney.models as models

from django.contrib.auth.models import User, Group

def check_group(user, gid):
    if not user.groups.filter(id=gid).exists():
        print(user.groups.filter(id=gid).exists())
        #raise Http404("{}".format(user.groups.all().values('id')))
        raise PermissionDenied("You are not in the right group to see this")

@login_required
def show_balance(request, gid):
    check_group(request.user, gid)
    users_balance = {}
    group_users = models.User.objects.filter(groups__id = gid)
    for u in group_users:
        users_balance[str(u)] = 0
    group_expenses = models.Expense.objects.filter(group__id = gid)
    for exp in group_expenses:
        sum_shares = sum(exp.shares.all().values_list("value", flat=True))
        for u in group_users:
            users_balance[str(u)] -= (exp.shares.get(owner=u).value/sum_shares)*exp.value
        users_balance[str(exp.origin)] += exp.value
    return HttpResponse(str(users_balance))


@login_required
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

@login_required
def show_user(request, uid):
    user = get_user()

@login_required
def edit_user(request, uid):
    pass

@login_required
def edit_group(request, uid):
    pass
