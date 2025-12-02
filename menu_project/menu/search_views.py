from django.http import JsonResponse
from django.db.models import Q
from .models import Category, MenuItem

def search_api(request):
    query = request.GET.get('q', '').strip()
    
    if not query or len(query) < 2:
        return JsonResponse({'results': []})
    
    results = []
    
    # 카테고리 검색
    categories = Category.objects.filter(
        Q(name__icontains=query)
    )[:5]
    
    for category in categories:
        results.append({
            'type': 'category',
            'title': category.name,
            'subtitle': '카테고리',
            'url': f'/menu/category/{category.id}/'
        })
    
    # 메뉴 검색
    menu_items = MenuItem.objects.filter(
        Q(name__icontains=query) | 
        Q(name_en__icontains=query) | 
        Q(description__icontains=query),
        is_available=True
    )[:5]
    
    for item in menu_items:
        results.append({
            'type': 'menu',
            'title': item.name,
            'subtitle': f'{item.category.name if item.category else "메뉴"} - ₩{item.price:,.0f}',
            'url': f'/menu/category/{item.category.id}/#menu-{item.id}' if item.category else f'/menu/#menu-{item.id}'
        })
    
    return JsonResponse({'results': results[:8]})
