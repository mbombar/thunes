from django.views import View
from django.urls import reverse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import DiscordWebhook
from .forms import WebhookForm

@method_decorator(login_required, name='dispatch')
class CreateWebhook(View):
    def post(self, request):
        form = WebhookForm(request.POST)

        if form.is_valid():
            webhook = form.cleaned_data["webhook"]
            group = form.cleaned_data["group"]

            if not request.user.groups.filter(id=group.id).exists():
                raise PermissionDenied("You are not in the right group to see this")

            if not webhook.startswith("https://discord.com/api/webhooks/"):
                raise Exception # on fait quoi là ?

            res = webhook.split("/")
            DiscordWebhook.objects.create(snowflake=res[-2],
                                          token=res[-1],
                                          group=group)

            return redirect(reverse("MyMoney:balance", kwargs={'gid': group.id}))
        else:
            raise Http404("Group not found")

@method_decorator(login_required, name='dispatch')
class DeleteWebhook(View):
    def post(self, request, webhook_id):
        hook = DiscordWebhook.objects.get(pk=webhook_id)
        gid = hook.group.id
        hook.delete()

        return redirect(reverse("MyMoney:balance", kwargs={'gid': gid}))
