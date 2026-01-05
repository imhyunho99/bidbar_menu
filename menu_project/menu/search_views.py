from django.http import JsonResponse
from django.db.models import Q
from .models import Category, MenuItem
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

def search_redirect_view(request):
    query = request.GET.get('q', '').strip()

    if not query:
        return redirect('menu:menu_main')

    # First, try to find an exact match (case-insensitive)
    menu_item = MenuItem.objects.filter(name__iexact=query).first()

    # If no exact match, try a contains match
    if not menu_item:
        menu_item = MenuItem.objects.filter(name__icontains=query).first()

    if menu_item:
        # If the item has a category, redirect to the category list page
        if menu_item.category:
            url = reverse('menu:menu_list', args=[menu_item.category.id])
            return redirect(f'{url}?target={menu_item.id}')
        else:
            messages.info(request, f"'{menu_item.name}' 메뉴를 찾았지만, 카테고리에 속해있지 않습니다.")
            return redirect('menu:menu_main')
    else:
        messages.warning(request, f"'{query}'에 해당하는 메뉴를 찾을 수 없습니다.")
        return redirect('menu:menu_main')


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
            'url': f'/category/{category.id}/'
        })
    
    # 메뉴 검색
    menu_items = MenuItem.objects.filter(
        Q(name__icontains=query) | 
        Q(name_en__icontains=query) | 
        Q(description__icontains=query),
        is_available=True
    )[:5]
    
    for item in menu_items:
        try:
            # Clean and convert price to float for formatting
            price_float = float(str(item.price).replace(',', ''))
            price_formatted = f"₩{price_float:,.0f}"
        except (ValueError, TypeError):
            # If conversion fails, fall back to using the original string
            price_formatted = f"₩{item.price}"

        results.append({
            'type': 'menu',
            'title': item.name,
            'subtitle': f'{item.category.name if item.category else "메뉴"} - {price_formatted}',
            'url': f'/category/{item.category.id}/#menu-{item.id}' if item.category else f'/#menu-{item.id}'
        })
    
    return JsonResponse({'results': results[:8]})