from django.contrib import admin
from .models import Category, MenuItem, SiteSettings

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'created_at', 'updated_at']
    fieldsets = (
        ('이미지/비디오 설정', {
            'fields': ('intro_image', 'intro_video', 'side_image')
        }),
        ('메뉴명(한글) 스타일', {
            'fields': ('menu_name_font', 'menu_name_color')
        }),
        ('메뉴명(영문) 스타일', {
            'fields': ('menu_name_en_font', 'menu_name_en_color')
        }),
        ('가격 스타일', {
            'fields': ('menu_price_font', 'menu_price_color')
        }),
        ('메뉴 설명 스타일', {
            'fields': ('menu_description_font', 'menu_description_color')
        }),
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'priority', 'parent']
    list_filter = ['parent']
    list_editable = ['priority']
    ordering = ['priority', 'name']

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'priority', 'price', 'category', 'is_available']
    list_filter = ['category', 'is_available']
    search_fields = ['name', 'description']
    list_editable = ['priority']
