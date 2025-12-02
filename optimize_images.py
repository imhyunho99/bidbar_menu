from PIL import Image
import os
from pathlib import Path

def optimize_image(image_path, max_width=1200, quality=85):
    """이미지 최적화"""
    try:
        img = Image.open(image_path)
        original_size = os.path.getsize(image_path)
        
        # RGBA를 RGB로 변환
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        
        # 리사이즈
        if img.width > max_width:
            ratio = max_width / img.width
            new_height = int(img.height * ratio)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
        
        # 저장
        img.save(image_path, format='JPEG', quality=quality, optimize=True)
        new_size = os.path.getsize(image_path)
        
        print(f"✓ {image_path.name}: {original_size/1024/1024:.2f}MB → {new_size/1024/1024:.2f}MB")
    except Exception as e:
        print(f"✗ {image_path.name}: {e}")

# static 폴더 이미지 최적화
static_dir = Path('menu_project/static')
for img_file in static_dir.glob('*.png'):
    optimize_image(img_file, max_width=1200, quality=85)
for img_file in static_dir.glob('*.jpg'):
    optimize_image(img_file, max_width=1200, quality=85)

print("\n완료!")
