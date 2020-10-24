from django.core.cache import cache

from MyMoney.models import Expense, Share

def invalidate_cache_on_update(sender, **kwargs):
    if sender in [Expense, Share]:

        # "instance" est l'objet modifié, même sur un signal post_delete
        # et Share dépend de Expense, donc on peut remonter share.expense.id
        # même quand l'objet vient de se faire supprimer (puisque Expense sera supprimé après)
        if sender is Expense:
            transaction = kwargs.get("instance", None)
            gid = transaction.group.id

        if sender is Share:
            share = kwargs.get("instance", None)
            gid = share.expense.group.id

        users_balance_key = f"show_balance_{gid}_user_balance"
        transactions_key  = f"show_balance_{gid}_transactions"
        expenses_key      = f"index_expense_{gid}_expenses"
        totalshare_key    = f"index_expense_{gid}_totalshare"

        users_balance = cache.delete(users_balance_key)
        transactions  = cache.delete(transactions_key)
        expenses      = cache.delete(expenses_key)
        totalshare    = cache.delete(totalshare_key)
