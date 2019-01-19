


from django import forms
from django.forms import ModelForm, Form, ModelMultipleChoiceField


from .models import Group, User


class GroupCreateOrEditForm(forms.ModelForm):
    """Formulaire de création ou l'édition d'un groupe"""

    members = ModelMultipleChoiceField(queryset = User.objects.all())
    class Meta:
        model = Group
        fields = ['name',]
    
