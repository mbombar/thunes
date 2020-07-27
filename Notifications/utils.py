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
        old_share = old_shares.get(share.owner.username, 0)

        display_value = f"{share.value}"
        if change and share.value != old_share:
            # On fait le diff si c'est un changement
            display_value = f"~~{old_share}~~ → " + display_value
        elif share.value == 0:
            continue # On cache les parts nulle (sauf si elles ont changés)
        display_value = f"{share_amount:.2f}{symbol} ({display_value})"
        fields.append({
            "name": share.owner.username,
            "value": display_value,
            "inline": True
        })

    group_url = settings.BASE_DOMAIN + reverse('MyMoney:balance',
                                               kwargs={'gid': transaction.group.id})

    title = f"{transaction.value}{symbol}"
    if change:
        message = "Modification d'une dépense"
        color = "16763648"
        if transaction.value != old_value:
            title = f"~~{old_value}{symbol}~~ → " + title
    else:
        message = "Nouvelle dépense"
        color = "65331"
    title = f"{transaction.name}: " + title

    req = {
        "content": message,
        "embeds": [{
            "title": title,
            "author": { "name": transaction.origin.username },
            "description": transaction.description,
            "url": group_url,
            "timestamp": transaction.date.isoformat(),
            "color": color,
            "fields": fields
        }]
    }

    # Et on l'envoie, à tous les webhook de ce groupe
    for webhook in DiscordWebhook.objects.filter(group=transaction.group):
        requests.post(webhook.get_url(), json=req)
