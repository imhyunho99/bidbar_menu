from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
import os

def optimize_image(image_field, max_width=1200, quality=85):
    """이미지 최적화: 리사이즈 및 압축 (원본 포맷 유지)"""
    if not image_field:
        return image_field
    
    img = Image.open(image_field)
    original_format = img.format or 'JPEG'
    file_ext = os.path.splitext(image_field.name)[1].lower()
    
    # 원본 파일명 유지
    original_name = image_field.name
    
    # PNG 또는 투명도가 있는 이미지는 그대로 유지
    if original_format == 'PNG' or img.mode in ('RGBA', 'LA', 'P'):
        if img.mode == 'P':
            img = img.convert('RGBA')
        
        # 리사이즈
        if img.width > max_width:
            ratio = max_width / img.width
            new_height = int(img.height * ratio)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
        
        # PNG로 저장
        output = BytesIO()
        img.save(output, format='PNG', optimize=True)
        output.seek(0)
        
        return InMemoryUploadedFile(
            output, 'ImageField',
            original_name,
            'image/png',
            sys.getsizeof(output), None
        )
    
    # JPEG 또는 기타 포맷
    else:
        # RGB로 변환
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # 리사이즈
        if img.width > max_width:
            ratio = max_width / img.width
            new_height = int(img.height * ratio)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
        
        # JPEG로 저장
        output = BytesIO()
        img.save(output, format='JPEG', quality=quality, optimize=True)
        output.seek(0)
        
        # 확장자가 jpg/jpeg가 아니면 .jpg로 변경
        if file_ext not in ['.jpg', '.jpeg']:
            original_name = f"{os.path.splitext(original_name)[0]}.jpg"
        
        return InMemoryUploadedFile(
            output, 'ImageField',
            original_name,
            'image/jpeg',
            sys.getsizeof(output), None
        )
