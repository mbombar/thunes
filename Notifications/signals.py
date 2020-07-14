from django.conf import settings
from django.urls import reverse
from django.db import transaction

from MyMoney.models import Expense, Share

import requests


def discord_notification(sender, **kwargs):
    transaction.on_commit(lambda: _discord_notification(sender, **kwargs))

def _discord_notification(sender, **kwargs):
    if sender != Expense:
        return

    if not kwargs.get("created", False):
        return

    transaction = kwargs.get("instance", None)
    shares = Share.objects.filter(expense=transaction);
    total = 0
    for share in shares:
        total += share.value
    base_value = transaction.value / total

    fields = []
    for share in shares:
        if share.value == 0:
            continue
        share_value = base_value * share.value
        fields.append({
            "name": f"{share.owner.username}",
            "value": f"{share_value:.2f}{transaction.currency.symbol} ({share.value})",
            "inline": True
        })

    group_url = reverse('MyMoney:balance', kwargs={'gid': transaction.group.id})

    req = {
        "embeds": [{
            "title": f"{transaction.name} ({transaction.value}{transaction.currency.symbol})",
            "author": {"name": f"{transaction.origin.username}"},
            "description": f"{transaction.description}",
            "url": f"{settings.BASE_DOMAIN}{group_url}",
            "timestamp": f"{transaction.date.isoformat()}",
            "color": 65331,
            "fields": fields
        }]
    }

    requests.post(settings.DISCORD_WEBHOOK_URL, json=req)
