from functools import wraps
from django.core.exceptions import PermissionDenied



def check_group(*args, **kwargs):
    """Décorateur pour checker si un utilisateur est dans le groupe
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, gid, *args, **kwargs):
            if not request.user.groups.filter(id=gid).exists():
                raise PermissionDenied("You are not in the right group to see this")
            return view_func(request, gid, *args, **kwargs)
        return _wrapped_view
    return decorator
