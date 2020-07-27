import requests

from django.conf import settings
from django.urls import reverse

from MyMoney.models import Expense, Share
from .models import DiscordWebhook


def send_notification(transaction, change=False, **kwargs):
    """Envoie des notifications"""

    symbol = transaction.currency.symbol
    shares = transaction.share_set.all()

    old_shares = kwargs.get("old_shares", {})
    old_value = kwargs.get("old_value", 0)

    # Calcul des montants propres des parts
    total = 0
    for share in shares:
        total += share.value
    base_value = transaction.value / total

    fields = []
    for share in shares:
        share_amount = base_value * share.value
        old_amount = base_value * old_shares.get(share.owner.username, 0)
        if change and share_amount != old_amount:
            # On fait le diff si c'est un changement
            value = f"~~{old_amount}{symbol}~~ → {share_amount:.2f}{symbol}"
        elif share.value != 0:
            value = f"{share_amount:.2f}{symbol}"
        else:
            continue # Do not display empty shares
        value += f" ({share.value})"
        fields.append({
            "name": f"{share.owner.username}",
            "value": value,
            "inline": True
        })

    group_url = settings.BASE_DOMAIN + reverse('MyMoney:balance',
                                               kwargs={'gid': transaction.group.id})

    title = f"{transaction.value}{symbol}"
    if change:
        message = "Modification"
        if transaction.value != old_value:
            title = "~~{old_value}{symbol}~~ → " + title
    else:
        message = "Création"
    title = f"{transaction.name}: " + title

    req = {
        "content": f"{message} d'une dépense",
        "embeds": [{
            "title": title,
            "author": {"name": f"{transaction.origin.username}"},
            "description": f"{transaction.description}",
            "url": group_url,
            "timestamp": f"{transaction.date.isoformat()}",
            "color": 65331,
            "fields": fields
        }]
    }

    # Et on l'envoie, à tous les webhook de ce groupe
    for webhook in DiscordWebhook.objects.filter(group=transaction.group):
        requests.post(webhook.get_url(), json=req)
