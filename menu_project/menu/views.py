from django.shortcuts import render
from .models import MenuItem, Category

def menu_list(request):
    categories = Category.objects.filter(parent=None)
    items = MenuItem.objects.filter(is_available=True)
    return render(request, 'menu/menu_list.html', {
        'categories': categories,
        'items': items
    })