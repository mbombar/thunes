from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from django.core.exceptions import ValidationError

from MyMoney.utils import add_to_group

from .models import (
    Group,
    User,
)

from .forms import (
    GroupCreateOrEditForm,
    UserCreationFormWithEmail,
)

# from .forms import (
#     GroupCreateOrEditForm,
# )

# Create your views here.

@login_required
def create_user(request):
    """Create a new user"""
    if request.method == 'GET':
        form = UserCreationFormWithEmail
        return render(request, 'users/create_user.html', {'form': form})
    elif request.method == 'POST':
        form = UserCreationFormWithEmail(request.POST)
        if form.is_valid():
            # raise ValidationError("'%(path)s'", code='path', params = {'path': form['username'].value()})
            username = form['username'].value()
            email = form['email'].value()
            form.save()
            new_user = User.objects.get(username=username)
            new_user.email = email
            new_user.save()
            return redirect("/")
        else:
            return render(request, 'users/create_user.html', {'form': form})

@login_required
def create_edit_group(request, gid=None):
    """Create a new group"""
    if request.method == 'GET':
        if gid:
            form = GroupCreateOrEditForm(instance=get_object_or_404(Group, id=gid))
        else:
            form = GroupCreateOrEditForm
        return render(request, 'users/create_group.html', {'form': form})
    elif request.method == 'POST':
        if gid:
            form = GroupCreateOrEditForm(request.POST, instance=get_object_or_404(Group, id=gid))
        else:
            form = GroupCreateOrEditForm(request.POST)
        # raise ValidationError("'%(path)s'", code='path', params = {'path': request.POST})
        members = request.POST.getlist('members')
        # raise ValidationError("'%(path)s'", code='path', params = {'path': members})
        queryset = User.objects.filter(id__in=members)
        # raise ValidationError("'%(members)s'", code='path', params = {'members': members})
        if form.is_valid():
            group = form.save()
            if gid:
                old_members = get_object_or_404(Group, id=gid).user_set.all()
                if set(old_members) <=  set(queryset):
                    for u in queryset.difference(old_members):
                        add_to_group(u, group)
                else:
                    form.add_error("members", "Ne retire pas de membres pauvre fou !")
                    return render(request, 'users/create_group.html', {'form': form})
            group.user_set.set(queryset)
            group.save()
            # raise ValidationError("'%(path)s'", code='path', params = {'path': request.POST})
            return redirect(reverse(
                'Users:groups',
            ))
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
