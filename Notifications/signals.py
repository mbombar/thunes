from django.conf import settings
from django.urls import reverse
from django.db import transaction

from MyMoney.models import Expense, Share
from .models import DiscordWebhook

import requests


# On diffère l'envoi de la notification à la fin de la transaction (s'il y en a une)
# pour avoir toutes les données correspondantes (sinon par exemple les 'Share' sont
# sauvegardées après la 'Expense' dont elles font partie)
# Lorsque l'on modifie une 'Expense' et qu'on veut une notification, il faut donc bien
# penser à mettre cette modification dans une transaction atomique avec toutes les
# modifications de 'Share' (ou autre) liées.
def discord_notification(sender, **kwargs):
    transaction.on_commit(lambda: _discord_notification(sender, **kwargs))

def _discord_notification(sender, **kwargs):
    if sender != Expense:
        return

    if not kwargs.get("created", False):
        return

    # On récupère l'objet qui vient d'être sauvegardé, ainsi que toutes les parts correspondantes
    transaction = kwargs.get("instance", None)
    shares = Share.objects.filter(expense=transaction);

    # Calcul des montants propres des parts
    total = 0
    for share in shares:
        total += share.value
    base_value = transaction.value / total

    # On remplit l'objet json qui indique à Discord comment formatter le message,
    # cf https://discord.com/developers/docs/resources/webhook#execute-webhook,
    # https://discord.com/developers/docs/resources/channel#embed-object,
    # et https://discord.com/developers/docs/resources/channel#embed-object-embed-field-structure
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

    # Et on l'envoie, à tous les webhook de ce groupe
    for webhook in DiscordWebhook.objects.filter(group=transaction.group):
        requests.post(webhook.get_url(), json=req)
