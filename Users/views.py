from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required


from .models import (
    Group,
    User,
)

# from .forms import (
#     GroupCreateOrEditForm,
# )

# Create your views here.

@login_required
def index_users(request):
    """Affiche la liste des utilisateurs"""
    users = User.objects.all()
    return render(request, 'users/index_users.html', {'users': users})
