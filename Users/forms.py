


from django import forms
from django.forms import ModelForm, Form, ModelMultipleChoiceField

from django.contrib.auth.forms import UserCreationForm

from .models import Group, User


class UserCreationFormWithEmail(UserCreationForm):
    email = forms.EmailField(label='Email', required=False)



class GroupCreateOrEditForm(forms.ModelForm):
    """Formulaire de création ou l'édition d'un groupe"""

    members = ModelMultipleChoiceField(queryset = User.objects.all(), widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Group
        fields = ['name',]

