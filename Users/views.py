from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from django.core.exceptions import ValidationError


from .models import (
    Group,
    User,
)

from .forms import (
    GroupCreateOrEditForm,
)

# from .forms import (
#     GroupCreateOrEditForm,
# )

# Create your views here.

@login_required
def create_user(request):
    """Create a new user"""
    if request.method == 'GET':
        form = UserCreationForm
        return render(request, 'users/create_user.html', {'form': form})
    elif request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
        else:
            return render(request, 'users/create_user.html', {'form': form})

@login_required
def create_group(request):
    """Create a new group"""
    if request.method == 'GET':
        form = GroupCreateOrEditForm
        return render(request, 'users/create_group.html', {'form': form})
    elif request.method == 'POST':
        form = GroupCreateOrEditForm(request.POST)
        # raise ValidationError("'%(path)s'", code='path', params = {'path': request.POST})
        members = request.POST.getlist('members')
        # raise ValidationError("'%(path)s'", code='path', params = {'path': members})
        queryset = User.objects.filter(id__in=members)
        # raise ValidationError("'%(members)s'", code='path', params = {'members': members})
        if form.is_valid():
            group = form.save()
            group.user_set.set(queryset)
            group.save()
            # raise ValidationError("'%(path)s'", code='path', params = {'path': request.POST})
            return redirect("/")
        else:
            return render(request, 'users/create_group.html', {'form': form})



@login_required
def index_users(request):
    """Affiche la liste des utilisateurs"""
    users = User.objects.all()
    return render(request, 'users/index_users.html', {'users': users})

@login_required
def index_groups(request):
    """Affiche la liste des groupes de l'utilisateur qui a fait la requête"""
    groups = request.user.groups.all()
    return render(request, 'users/index_groups.html', {'groups': groups})
