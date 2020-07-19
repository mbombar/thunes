from django import forms
from django.contrib.auth.models import Group
from .models import DiscordWebhook

from django.core.exceptions import ValidationError

class WebhookForm(forms.Form):
    webhook = forms.URLField(label='Webhook URL')
    group = forms.ModelChoiceField(queryset=Group.objects.all(),
                                   widget=forms.HiddenInput)
