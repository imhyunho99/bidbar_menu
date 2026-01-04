from django.urls import path
from . import views, webhook_views

app_name = 'menu'

urlpatterns = [
    path('', views.menu_main, name='menu_main'),
    path('category/<int:category_id>/', views.menu_list, name='menu_list'),
    path('api/search/', views.search_api, name='search_api'),
    path('webhook/github/', webhook_views.github_webhook, name='github_webhook'),
]
