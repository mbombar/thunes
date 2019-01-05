


from django import forms
from django.forms import ModelForm, Form


from .models import Group


class GroupCreateOrEditForm(forms.ModelForm):
    """Formulaire de création ou l'édition d'un groupe"""

    class Meta:
        model = Group
        fields = '__all__'

    
