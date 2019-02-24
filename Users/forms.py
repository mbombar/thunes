


from django import forms
from django.forms import ModelForm, Form, ModelMultipleChoiceField

from django.contrib.auth.forms import UserCreationForm

from .models import Group, User


class UserCreationFormWithEmail(UserCreationForm):
    email = forms.EmailField(label='Email', required=False)



class GroupCreateOrEditForm(forms.ModelForm):
    """Formulaire de création ou l'édition d'un groupe"""
    def __init__(self, *args, **kwargs):
        super(GroupCreateOrEditForm, self).__init__(*args, **kwargs)
        try:
            self.fields['members'].initial = self.instance.user_set.all()
            self.fields['name'].widget.attrs['readonly'] = 'true'
        except:
            pass
    members = ModelMultipleChoiceField(queryset = User.objects.all(), widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Group
        fields = ['name',]

