#!/bin/bash

# 배포 스크립트 - 서버에서 실행될 스크립트
# 경로: /home/ubuntu/deploy.sh

set -e  # 에러 발생 시 스크립트 중단

LOG_FILE="/home/ubuntu/deploy.log"
PROJECT_DIR="/home/ubuntu/bidbar_menu"

echo "$(date): Starting deployment..." >> $LOG_FILE

# 프로젝트 디렉토리로 이동
cd $PROJECT_DIR

# Git pull
echo "$(date): Pulling latest changes..." >> $LOG_FILE
git pull origin main >> $LOG_FILE 2>&1

# 가상환경 활성화 및 의존성 설치
echo "$(date): Installing dependencies..." >> $LOG_FILE
source venv/bin/activate
pip install -r requirements.txt >> $LOG_FILE 2>&1

# Django 마이그레이션
echo "$(date): Running migrations..." >> $LOG_FILE
cd menu_project
python manage.py migrate >> $LOG_FILE 2>&1

# 정적 파일 수집
echo "$(date): Collecting static files..." >> $LOG_FILE
python manage.py collectstatic --noinput >> $LOG_FILE 2>&1

# uWSGI 재시작
echo "$(date): Restarting uWSGI..." >> $LOG_FILE
sudo systemctl restart uwsgi >> $LOG_FILE 2>&1

# Nginx 재로드 (필요시)
echo "$(date): Reloading Nginx..." >> $LOG_FILE
sudo systemctl reload nginx >> $LOG_FILE 2>&1

echo "$(date): Deployment completed successfully!" >> $LOG_FILE
