from django.db import models
from django.contrib.auth.models import User, Group


class Currency(models.Model):
    name = models.CharField(max_length=3)
    symbol = models.CharField(max_length=1, null=True, blank=True)
    value_in_eur = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return "{} ({})".format(self.name, self.symbol)

class Transaction(models.Model):
    origin = models.ForeignKey(User, on_delete=models.PROTECT, related_name="origin")
    destination = models.ForeignKey(User, null=True, on_delete=models.PROTECT, related_name="destination")
    group = models.ForeignKey(Group, on_delete=models.PROTECT)
    description = models.TextField()
    value = models.DecimalField(decimal_places=2, max_digits=10)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
