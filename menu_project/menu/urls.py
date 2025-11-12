from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('', views.menu_main, name='menu_main'),
    path('category/<int:category_id>/', views.menu_list, name='menu_list'),
]
