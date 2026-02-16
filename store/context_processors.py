from .models import MenuItem

def menu_items(request):
    return {
        'menu_items': MenuItem.objects.filter(is_active=True)
    }