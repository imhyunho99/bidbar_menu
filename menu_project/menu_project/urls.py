from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from menu.qr_views import generate_qr_code

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('menu.urls')),  # 루트 URL을 메뉴로 설정
    path('qr/', generate_qr_code, name='qr_code'),
    path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'favicon.ico')),
]

# 개발 환경에서 미디어 파일 서빙
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
