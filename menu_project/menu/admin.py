from django.contrib import admin
from .models import Category, MenuItem, SiteSettings

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'created_at', 'updated_at']
    fields = ['intro_image']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent']

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'priority', 'price', 'category', 'is_available']
    list_filter = ['category', 'is_available']
    search_fields = ['name', 'description']
    list_editable = ['priority']
