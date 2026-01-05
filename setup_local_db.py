#!/usr/bin/env python3
"""
PostgreSQL 덤프를 Django 픽스처로 변환하는 스크립트
"""
import os
import sys
import django
from pathlib import Path

# Django 설정
sys.path.append('/Users/nahyeonho/pythonWorkspace/bidbar/menu_project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'menu_project.settings')
django.setup()

from django.core.management import call_command

def setup_local_db():
    """로컬 SQLite 데이터베이스 설정"""
    print("Creating SQLite database...")
    
    # 마이그레이션 실행
    call_command('migrate')
    
    # 슈퍼유저 생성 (선택사항)
    print("Database setup completed!")
    print("To create a superuser, run: python manage.py createsuperuser")

if __name__ == '__main__':
    setup_local_db()
