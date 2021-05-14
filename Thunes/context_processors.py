from . import settings

def debug(request):
    """Permet d'accéder à la variable debug dans les templates"""
    return {
        'debug': settings.DEBUG,
    }
