# menu/views.py
from rest_framework import viewsets, permissions
from.models import Menu
from.serializers import MenuSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class MenuViewSet(viewsets.ModelViewSet):
    """
    메뉴를 조회하거나 편집할 수 있는 API 엔드포인트입니다.
    """
    queryset = Menu.objects.all().order_by('-created_at')
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]