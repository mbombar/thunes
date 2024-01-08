from django.db import models

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group as DjangoGroup


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    favorite_groups = models.ManyToManyField(
        blank=True, to="Users.Group", related_name="favorite_groups"
    )


class Group(DjangoGroup):
    class Meta:
        proxy = True
