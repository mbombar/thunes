from django.db import models
from django.contrib.auth.models import User, Group


class DiscordWebhook(models.Model):

    name = models.CharField(max_length=50, blank=True)

    # Un snowflake est un entier 64 bits sous forme de chaine de caractères
    # normalement ça fait moins de 20 de longueur
    snowflake = models.CharField(max_length=20)
    # Quelle est la taille max d'un token ? à priori moins de 100...
    token = models.CharField(max_length=100)
    # On peut avoir plusieurs hook par group, ça sert à rien
    # (sauf si on aime vraiment les notifs), mais c'est pas génant
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def get_url(self):
        return "https://discord.com/api/webhooks/{}/{}".format(self.snowflake, self.token)

    def __str__(self):
        return "{}: {}/{}".format(self.name, self.snowflake, self.token)
