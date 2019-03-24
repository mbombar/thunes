from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

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

class Share(models.Model):
    value = models.DecimalField(decimal_places=2, max_digits=10)
    owner = models.ForeignKey(User, on_delete=models.PROTECT)

    # Content type pour avoir des ForeignKeys Polymorphes
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # Stocke les content_types pour chaque type d'objet qui va utiliser Share
    _content_types = dict()
    _content_types[Expense] = ContentType.objects.get_for_model(Expense)
    _content_types[FavoriteExpense] = ContentType.objects.get_for_model(FavoriteExpense)

    def __str__(self):
        return "{} {}".format(self.owner, self.value)

    @staticmethod
    def get_expense(expense):
        """
        Récupère les parts d'une Expense en particulier
        """
        return Share.objects.filter(content_type=Share._content_types[Expense], object_id=expense.pk)

    @staticmethod
    def get_favorite_expense(expense):
        """
        Récupère les parts d'une FavoriteExpense en particulier
        """

        return Share.objects.filter(content_type=Share._content_types[FavoriteExpense], object_id=expense.pk)
