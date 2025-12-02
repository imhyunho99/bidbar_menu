from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Category, MenuItem

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        messages.error(request, '관리자 권한이 없습니다.')
    return render(request, 'admin/login.html')

@login_required
def admin_dashboard(request):
    categories = Category.objects.all()
    menu_items = MenuItem.objects.all()
    return render(request, 'admin/dashboard.html', {
        'categories': categories,
        'menu_items': menu_items
    })

@login_required
def add_category(request):
    if request.method == 'POST':
        name = request.POST['name']
        parent_id = request.POST.get('parent')
        parent = Category.objects.get(id=parent_id) if parent_id else None
        Category.objects.create(name=name, parent=parent)
        return redirect('admin_dashboard')
    categories = Category.objects.filter(parent=None)
    return render(request, 'admin/add_category.html', {'categories': categories})

@login_required
def add_menu(request):
    if request.method == 'POST':
        MenuItem.objects.create(
            name=request.POST['name'],
            name_en=request.POST.get('name_en', ''),
            price=request.POST['price'],
            description=request.POST['description'],
            category_id=request.POST.get('category') or None,
            notes=request.POST.get('notes', ''),
            menu_image=request.FILES.get('image')
        )
        return redirect('admin_dashboard')
    categories = Category.objects.all()
    return render(request, 'admin/add_menu.html', {'categories': categories})

@login_required
def edit_menu(request, menu_id):
    menu = get_object_or_404(MenuItem, id=menu_id)
    if request.method == 'POST':
        menu.name = request.POST['name']
        menu.name_en = request.POST.get('name_en', '')
        menu.price = request.POST['price']
        menu.description = request.POST['description']
        menu.category_id = request.POST.get('category') or None
        menu.notes = request.POST.get('notes', '')
        if request.FILES.get('image'):
            menu.menu_image = request.FILES['image']
        menu.save()
        return redirect('admin_dashboard')
    categories = Category.objects.all()
    return render(request, 'admin/edit_menu.html', {'menu': menu, 'categories': categories})

@login_required
def delete_menu(request, menu_id):
    MenuItem.objects.filter(id=menu_id).delete()
    return redirect('admin_dashboard')

@login_required
def delete_category(request, category_id):
    Category.objects.filter(id=category_id).delete()
    return redirect('admin_dashboard')
