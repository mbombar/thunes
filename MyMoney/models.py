from django.db import models
from django.contrib.auth import User, Group


class Currency(models.Model):
    name = models.CharField(max_length=3)
    symbol = models.CharField(max_length=1)
    value_in_eur = models.DecimalField(decimal_places=2)

class Transaction(models.Model):
    origin = models.ForeignKey(User)
    destination = models.ForeignKey(User, null=True)
    group = models.ForeignKey(Group)
    description = models.TextField()
    value = model.DecimalField(decimal_places=2)
    currency = models.ForeignKey(Currency)
