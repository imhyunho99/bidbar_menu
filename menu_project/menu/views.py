from django.shortcuts import render
from .models import MenuItem, Category

def menu_list(request):
    # 모든 카테고리 (부모와 자식 모두)
    all_categories = Category.objects.all()
    # 사용 가능한 메뉴 아이템
    items = MenuItem.objects.filter(is_available=True).select_related('category')
    
    return render(request, 'menu/menu_list.html', {
        'categories': all_categories,
        'items': items
    })