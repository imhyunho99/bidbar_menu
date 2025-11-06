from django.urls import path
from . import views, qr_views

urlpatterns = [
    path('', views.menu_list, name='menu_list'),
    path('qr/', qr_views.generate_qr_code, name='qr_code'),
    path('mobile-test/', qr_views.mobile_test, name='mobile_test'),
]
