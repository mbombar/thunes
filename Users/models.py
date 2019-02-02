from django.db import models

# Create your models here.



from django.contrib.auth.models import Group, User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    favorite_groups = models.ManyToManyField(
        blank=True,
        to='Users.Group',
        related_name='favorite_groups')

class Group(Group):
    class Meta:
        proxy = True
