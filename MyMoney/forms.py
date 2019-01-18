from django import forms
from django.contrib.auth.models import User, Group

import MyMoney.models as models

from django.core.exceptions import ValidationError

# raise ValidationError("'%(path)s'", code='path', params = {'path': self.fields})

# class ShareForm(forms.ModelForm):
#     class Meta:
#         model = models.Share
#         fields = '__all__'

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = models.Expense
        fields = '__all__'
        exclude = ['group',]

    def __init__(self, *args, **kwargs):
        group = kwargs.pop('group', None)
        super(ExpenseForm, self).__init__(*args, **kwargs)
        self.fields['origin'].queryset = group.user_set.all()


class ShareForm(forms.ModelForm):
    # name = forms.CharField()
    class Meta:
        model = models.Share
        fields = [
            'value',
            'owner',
            # 'name',
            ]
    def __init__(self, *args, **kwargs):
        super(ShareForm, self).__init__(*args, **kwargs)
        self.fields['owner'].disabled = True
