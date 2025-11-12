# menu/models.py

from django.db import models

class Category(models.Model):
    """
    메뉴 카테고리 모델. 부모-자식 관계를 통해 계층 구조를 지원합니다.
    (예: 음료 > 커피 > 아이스 아메리카노)
    """
    name = models.CharField(max_length=100, verbose_name="카테고리명")
    # 'self'를 참조하여 부모 카테고리를 지정할 수 있습니다.
    # 최상위 카테고리(부모 카테고리)는 이 필드가 비어있게 됩니다.
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='sub_categories',
        verbose_name="부모 카테고리"
    )

    class Meta:
        verbose_name = "메뉴 카테고리"
        verbose_name_plural = "메뉴 카테고리"
        ordering = ['name']

    def __str__(self):
        # 부모 카테고리가 있는 경우 '부모 > 자식' 형태로 표시
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name

class MenuItem(models.Model):
    """
    개별 메뉴 항목에 대한 모델
    """
    # 1. 이름
    name = models.CharField(max_length=100, verbose_name="메뉴명")

    # 2. 가격
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="가격")

    # 3. 설명
    description = models.TextField(verbose_name="메뉴 설명")

    # 4. 카테고리 (부모/서브 카테고리)
    # Category 모델과 연결하여 메뉴의 소속 카테고리를 지정합니다.
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL, # 카테고리가 삭제되어도 메뉴는 유지 (카테고리 없음 상태로)
        null=True,
        blank=True,
        related_name='menu_items',
        verbose_name="카테고리"
    )

    # 5. 기타
    notes = models.TextField(blank=True, null=True, verbose_name="기타 사항")

    # 6. 설명 이미지
    # Pillow 라이브러리가 설치되어 있어야 합니다 (pip install Pillow)
    describe_image = models.ImageField(
        upload_to='menu_images/',
        blank=True,
        null=True,
        verbose_name="메뉴 이미지"
    )
    
    is_available = models.BooleanField(default=True, verbose_name="판매 가능 여부")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    class Meta:
        verbose_name = "메뉴 항목"
        verbose_name_plural = "메뉴 항목"
        ordering = ['name']

    def __str__(self):
        return self.name
    
    