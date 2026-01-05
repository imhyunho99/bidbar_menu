from django.urls import path
from . import views
from . import search_views

app_name = 'menu'

urlpatterns = [
    path('', views.menu_main, name='menu_main'),
    path('category/<int:category_id>/', views.menu_list, name='menu_list'),
    
    # API for AJAX search (will be removed from templates but kept for now)
    path('api/search/', search_views.search_api, name='search_api'),
    
    # New server-side search
    path('search/', search_views.search_redirect_view, name='search_redirect'),
]