from django.urls import reverse
from django.utils import timezone
from django.core.cache import cache
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory, formset_factory
from django.db.models import Sum

from fractions import Fraction

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

    users_balance_key = f"show_balance_{gid}_user_balance"
    transactions_key  = f"show_balance_{gid}_transactions"
    users_balance = cache.get(users_balance_key)
    transactions  = cache.get(transactions_key)

    if users_balance is None or transactions is None:
        users = User.objects.filter(groups=group)
        expenses = models.Expense.objects.filter(group=group)
        users_balance = {}

        for user in users:
            users_balance[user.username] = 0
            # User.username est une clef unique, on peut indexer sans soucis dessus

        for expense in expenses:
            shares = expense.share_set
            value = Fraction(int(expense.value * 100), 100)
            sum_shares = int(shares.aggregate(total=Sum("value")).get("total") * 100)

            users_balance[expense.origin.username] += value
            for user in users:
                share = shares.filter(owner=user)
                if share: # Si la share d'un user n'existe pas, elle vaut 0, on ignore
                    share = int(share.get().value * 100)
                    users_balance[user.username] -= value * Fraction(share, sum_shares)

        transactions = balance_transactions(users_balance)
        cache.set(users_balance_key, users_balance, None)
        cache.set(transactions_key, transactions, None)
        # Pas de timeout, on invalide manuellement

    context = {
        "balance": users_balance,
        "group": group,
        "transactions": transactions,
    }

    return render(request, "balance.html", context)


@login_required
@check_group()
def new_expense(request, gid):
    group = Group.objects.get(id=gid)
    n = group.user_set.count()
    if n == 0:
        raise Exception
    currency, _ = models.Currency.objects.get_or_create(name='Eur', defaults={'value_in_eur': 1})
    expense_form = ExpenseForm(request.POST or None, group=group,
                               initial={'origin': request.user,
                                        'currency' : currency})

    # On crée des parts à 0 pour tous les membres du groupe
    ShareFormSet = formset_factory(ShareForm, extra=0)
    share_formset = ShareFormSet(request.POST or None)

    if expense_form.is_valid() and share_formset.is_valid():
            expense = expense_form.save(commit=False)
            expense.group = group
            if not expense.date:
                expense.date = timezone.now()
            expense.save()

            for share_form in share_formset:
                share = share_form.save(commit=False)
                share.expense = expense
                share.save()

            return redirect(reverse(
                'MyMoney:balance',
                kwargs={'gid': gid}
            ))

    elif request.method != "GET":
        return render(request, "expense.html", {
            "expense_form": expense_form,
            "share_formset": share_formset,
            "group": group,
        })

    else:
        initial_share = []
        for user in group.user_set.all():
            initial_share.append({'value': 1, 'owner': user})
            share_formset = ShareFormSet(initial=initial_share)

        return render(request, "expense.html", {
            "expense_form": expense_form,
            "share_formset": share_formset,
            "group": group,
        }
        )


@login_required
@check_group()
def index_expense(request, gid):
    """Affiche l'historique des dépenses d'un groupe"""
    group = Group.objects.get(id=gid)
    expenses = models.Expense.objects.filter(group=group).order_by('-date')
    shares = [expense.share_set.all() for expense in expenses]
    totalshare = [sum([share.value for share in queryset]) for queryset in shares]
    return render(request, "index_expenses.html", {
        "expense_total": zip(expenses, totalshare),
        "group": group,
        "gid": gid,
        }
    )

@login_required
@check_group()
def rembourser(request, gid, user1, user2):
    group = Group.objects.get(id=gid)
    user1 = User.objects.get(username=user1)
    user2 = User.objects.get(username=user2)
    n = group.user_set.count()
    if n == 0:
        raise Exception

    if request.method == "GET":

        ShareFormSet = formset_factory(ShareForm, extra=0)

        initial_expense = {'name': 'Remboursement', 'origin': user1}
        expense_form = ExpenseForm(group=group, initial=initial_expense)

        # On crée une part à -1 pour l'user2, et à 0 pour le reste
        initial_share = [{'value': -1, 'owner': user2}]

        for user in group.user_set.exclude(username=user2.username):
            initial_share.append({'value': 0, 'owner': user})

        share_formset = ShareFormSet(initial=initial_share)

        return render(request, "expense.html", {
            "expense_form": expense_form,
            "share_formset": share_formset,
            "group": group,
        }
        )

    else:
        expense_form = ExpenseForm(request.POST or None, group=group)

        ShareFormSet = formset_factory(ShareForm, extra=0)
        share_formset = ShareFormSet(request.POST or None)

        if expense_form.is_valid():
            if share_formset.is_valid():
                expense = expense_form.save(commit=False)
                expense.group = group
                expense.save()

                for share_form in share_formset:
                    share = share_form.save(commit=False)
                    share.expense = expense
                    share.save()

                return redirect(reverse(
                    'MyMoney:balance',
                    kwargs={'gid': gid}
                ))

        else:
            return render(request, "expense.html", {
                "expense_form": expense_form,
                "share_formset": share_formset,
                "group": group,
            })
