from django import forms
from django.contrib.auth.models import User

import MyMoney.models as models

class ShareForm(forms.ModelForm):
    class Meta:
        model = models.Share
        fields = '__all__'

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = models.Expense
        fields = '__all__'
        exclude = ['group',]
    

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
        # gid = kwargs.get('gid')
        super(ShareForm, self).__init__(*args, **kwargs)
        # self.fields['owner'].queryset = User.objects.filter(groups__id=gid)
        # self.fields['name'] = str(owner)
