from django.db import models
from django.contrib.auth.models import User, Group


class Currency(models.Model):
    name = models.CharField(max_length=3)
    symbol = models.CharField(max_length=1, null=True, blank=True)
    value_in_eur = models.DecimalField(decimal_places=2, max_digits=10)

    class Meta:
        verbose_name = 'currency'
        verbose_name_plural = 'currencies'

    def __str__(self):
        return "{} ({})".format(self.name, self.symbol)

class Expense(models.Model):
    name = models.CharField(max_length=50)
    origin = models.ForeignKey(User, on_delete=models.PROTECT)
    group = models.ForeignKey(Group, on_delete=models.PROTECT)
    description = models.TextField(blank=True)
    value = models.DecimalField(decimal_places=2, max_digits=10)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    date = models.DateField(blank=True)

    def __str__(self):
        return "{}-{} ({}) {} {}".format(self.group, self.name, self.origin, self.value, self.currency)

    def delete(self, *args, **kwargs):
        shares = self.share_set.all()
        for share in shares:
            share.delete()
        super().delete(*args, **kwargs)

class Share(models.Model):
    value = models.DecimalField(decimal_places=2, max_digits=10)
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    expense = models.ForeignKey(Expense, on_delete=models.PROTECT)

    def __str__(self):
        return "{} {}".format(self.owner, self.value)
