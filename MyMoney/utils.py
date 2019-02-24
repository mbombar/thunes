import MyMoney.models as models
import MyMoney.forms as forms

from django.core.exceptions import ValidationError

def add_to_group(user, group):
    """
    Ajoute un user dans un groupe en ajoutant des parts à 0
    dans les transactions précédentes du groupe.
    """
    group_expenses = models.Expense.objects.filter(group__id=group.id)
    for exp in group_expenses:
        new_share = models.Share()
        new_share.expense = exp
        new_share.owner = user
        new_share.value = 0
        new_share.save()

def del_from_group(user, group):
    pass

