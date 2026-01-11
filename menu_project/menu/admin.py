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
            'fields': ('menu_name_font', 'menu_name_color', 'menu_name_size', 'menu_name_bold', 'menu_name_italic')
        }),
        ('메뉴명(영문) 스타일', {
            'fields': ('menu_name_en_font', 'menu_name_en_color', 'menu_name_en_size', 'menu_name_en_bold', 'menu_name_en_italic')
        }),
        ('가격 스타일', {
            'fields': ('menu_price_font', 'menu_price_color', 'menu_price_size', 'menu_price_bold', 'menu_price_italic')
        }),
        ('메뉴 설명 스타일', {
            'fields': ('menu_description_font', 'menu_description_color', 'menu_description_size', 'menu_description_bold', 'menu_description_italic')
        }),
    )

from django.contrib import admin
from django import forms
from .models import Category, MenuItem, SiteSettings

class CategoryAdminForm(forms.ModelForm):
    name = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}))
    
    class Meta:
        model = Category
        fields = '__all__'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
    list_display = ['name', 'name_en', 'priority', 'parent']
    list_filter = ['parent']
    list_editable = ['priority']
    ordering = ['priority', 'name']
    fields = ['name_en', 'name', 'priority', 'parent', 'category_image', 'hide_side_image']

class MenuItemAdminForm(forms.ModelForm):
    name = forms.CharField(widget=forms.Textarea(attrs={'rows':3, 'cols': 40}), label="메뉴명")
    name_en = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}), label="메뉴명(영문)", required=False)

    class Meta:
        model = MenuItem
        fields = '__all__'

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    form = MenuItemAdminForm
    list_display = ['name', 'priority', 'price', 'category', 'is_available']
    list_filter = ['category', 'is_available']
    search_fields = ['name', 'description']
    list_editable = ['priority']
    fields = ['name_en', 'name', 'price', 'description', 'category', 'notes', 'menu_image', 'priority', 'is_available']
