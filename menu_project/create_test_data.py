#!/usr/bin/env python
import os
import sys
import django

# Django 설정
sys.path.append('/Users/nahyeonho/pythonWorkspace/bidbar/menu_project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'menu_project.settings')
django.setup()

from menu.models import Category, MenuItem

def create_test_data():
    # 기존 데이터 삭제
    MenuItem.objects.all().delete()
    Category.objects.all().delete()
    
    # 카테고리 생성
    categories = {
        '음료': Category.objects.create(name='음료'),
        '식사': Category.objects.create(name='식사'),
        '디저트': Category.objects.create(name='디저트'),
        '주류': Category.objects.create(name='주류')
    }
    
    # 서브 카테고리 생성
    sub_categories = {
        '커피': Category.objects.create(name='커피', parent=categories['음료']),
        '차': Category.objects.create(name='차', parent=categories['음료']),
        '주식': Category.objects.create(name='주식', parent=categories['식사']),
        '안주': Category.objects.create(name='안주', parent=categories['식사']),
        '케이크': Category.objects.create(name='케이크', parent=categories['디저트']),
        '맥주': Category.objects.create(name='맥주', parent=categories['주류']),
        '소주': Category.objects.create(name='소주', parent=categories['주류'])
    }
    
    # 메뉴 아이템 생성
    menu_items = [
        # 커피
        {'name': '아메리카노', 'price': 4500, 'description': '깊고 진한 에스프레소의 풍미', 'category': sub_categories['커피']},
        {'name': '카페라떼', 'price': 5000, 'description': '부드러운 우유와 에스프레소의 조화', 'category': sub_categories['커피']},
        {'name': '카푸치노', 'price': 5500, 'description': '풍성한 거품과 진한 커피의 만남', 'category': sub_categories['커피']},
        {'name': '바닐라라떼', 'price': 5500, 'description': '달콤한 바닐라 향이 가득한 라떼', 'category': sub_categories['커피']},
        
        # 차
        {'name': '얼그레이', 'price': 4000, 'description': '베르가못 향이 은은한 홍차', 'category': sub_categories['차']},
        {'name': '캐모마일', 'price': 4000, 'description': '마음을 편안하게 해주는 허브차', 'category': sub_categories['차']},
        {'name': '녹차', 'price': 3500, 'description': '깔끔하고 담백한 우리나라 전통차', 'category': sub_categories['차']},
        
        # 주식
        {'name': '파스타 알리오올리오', 'price': 12000, 'description': '마늘과 올리브오일의 심플한 맛', 'category': sub_categories['주식']},
        {'name': '크림파스타', 'price': 13000, 'description': '진한 크림소스와 베이컨의 조화', 'category': sub_categories['주식']},
        {'name': '리조또', 'price': 14000, 'description': '치즈와 버섯이 들어간 이탈리아 쌀요리', 'category': sub_categories['주식']},
        {'name': '스테이크', 'price': 25000, 'description': '부드러운 안심 스테이크 200g', 'category': sub_categories['주식']},
        
        # 안주
        {'name': '치킨윙', 'price': 8000, 'description': '바삭한 치킨윙 6조각', 'category': sub_categories['안주']},
        {'name': '감자튀김', 'price': 6000, 'description': '바삭바삭한 감자튀김', 'category': sub_categories['안주']},
        {'name': '치즈볼', 'price': 7000, 'description': '쫄깃한 치즈가 들어간 볼', 'category': sub_categories['안주']},
        {'name': '오징어링', 'price': 9000, 'description': '바삭한 오징어링과 타르타르소스', 'category': sub_categories['안주']},
        
        # 케이크
        {'name': '초콜릿케이크', 'price': 6000, 'description': '진한 초콜릿의 달콤함', 'category': sub_categories['케이크']},
        {'name': '치즈케이크', 'price': 6500, 'description': '부드러운 크림치즈케이크', 'category': sub_categories['케이크']},
        {'name': '티라미수', 'price': 7000, 'description': '이탈리아 전통 디저트', 'category': sub_categories['케이크']},
        
        # 맥주
        {'name': '생맥주', 'price': 4000, 'description': '시원하고 깔끔한 생맥주 500ml', 'category': sub_categories['맥주']},
        {'name': 'IPA', 'price': 6000, 'description': '홉의 쌉쌀한 맛이 특징인 수제맥주', 'category': sub_categories['맥주']},
        {'name': '밀맥주', 'price': 5500, 'description': '부드럽고 달콤한 밀맥주', 'category': sub_categories['맥주']},
        
        # 소주
        {'name': '참이슬', 'price': 4000, 'description': '깔끔한 맛의 대표 소주', 'category': sub_categories['소주']},
        {'name': '처음처럼', 'price': 4000, 'description': '순하고 부드러운 소주', 'category': sub_categories['소주']},
    ]
    
    for item_data in menu_items:
        MenuItem.objects.create(**item_data)
    
    print("테스트 데이터가 성공적으로 생성되었습니다!")
    print(f"카테고리: {Category.objects.count()}개")
    print(f"메뉴 아이템: {MenuItem.objects.count()}개")

if __name__ == '__main__':
    create_test_data()
