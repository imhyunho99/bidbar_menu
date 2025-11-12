from django.shortcuts import render, get_object_or_404
from .models import MenuItem, Category

def get_breadcrumb_path(category):
    """카테고리의 전체 경로를 생성"""
    path = []
    current = category
    while current:
        path.insert(0, current)
        current = current.parent
    return path

def menu_main(request):
    # 최상위 카테고리만 가져오기 (parent가 None인 카테고리)
    top_categories = Category.objects.filter(parent=None)
    
    return render(request, 'menu/menu_main.html', {
        'categories': top_categories
    })

def menu_list(request, category_id):
    # 선택된 카테고리
    category = get_object_or_404(Category, id=category_id)
    sub_categories = category.sub_categories.all()
    breadcrumb_path = get_breadcrumb_path(category)
    
    # 하위 카테고리가 있으면 카테고리 페이지, 없으면 메뉴 페이지
    if sub_categories.exists():
        # 하위 카테고리가 있는 경우 - 카테고리 선택 페이지
        return render(request, 'menu/category_list.html', {
            'category': category,
            'categories': sub_categories,
            'breadcrumb_path': breadcrumb_path
        })
    else:
        # 최하위 카테고리인 경우 - 메뉴 표시
        items = MenuItem.objects.filter(category=category, is_available=True)
        return render(request, 'menu/menu_list.html', {
            'category': category,
            'items': items,
            'breadcrumb_path': breadcrumb_path
        })