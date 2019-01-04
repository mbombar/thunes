from django import forms
from django.contrib.auth.models import User

import MyMoney.models as models

class ShareForm(forms.ModelForm):
    class Meta:
        model = models.Share
        fields = ["value", "owner"]

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = models.Expense
        fields = ["name", "description", "value", "currency"]
    shares_fields = []
    
