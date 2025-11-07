from django.urls import path
from . import views, qr_views, admin_views

urlpatterns = [
    path('', views.menu_list, name='menu_list'),
    path('qr/', qr_views.generate_qr_code, name='qr_code'),
    path('mobile-test/', qr_views.mobile_test, name='mobile_test'),
    
    # Admin URLs
    path('admin-login/', admin_views.admin_login, name='admin_login'),
    path('admin/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('admin/add-category/', admin_views.add_category, name='add_category'),
    path('admin/add-menu/', admin_views.add_menu, name='add_menu'),
    path('admin/edit-menu/<int:menu_id>/', admin_views.edit_menu, name='edit_menu'),
    path('admin/delete-menu/<int:menu_id>/', admin_views.delete_menu, name='delete_menu'),
    path('admin/delete-category/<int:category_id>/', admin_views.delete_category, name='delete_category'),
]
