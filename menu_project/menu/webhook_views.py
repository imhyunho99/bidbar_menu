import json
import subprocess
import threading
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import logging

logger = logging.getLogger(__name__)

def deploy_in_background():
    """백그라운드에서 배포 실행"""
    try:
        # 배포 스크립트 실행 (서버에 deploy.sh가 있다고 가정)
        result = subprocess.run([
            'bash', '/home/ubuntu/deploy.sh'
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            logger.info("Deployment successful")
        else:
            logger.error(f"Deployment failed: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        logger.error("Deployment timed out")
    except Exception as e:
        logger.error(f"Deployment error: {str(e)}")

@csrf_exempt
@require_http_methods(["POST"])
def github_webhook(request):
    """GitHub 웹훅 엔드포인트 - 즉시 응답하고 백그라운드에서 배포"""
    try:
        # GitHub 웹훅 페이로드 검증 (선택사항)
        payload = json.loads(request.body)
        
        # main 브랜치 push만 처리
        if payload.get('ref') == 'refs/heads/main':
            # 백그라운드에서 배포 실행
            thread = threading.Thread(target=deploy_in_background)
            thread.daemon = True
            thread.start()
            
            logger.info("Deployment started in background")
            return JsonResponse({'status': 'deployment_started'})
        else:
            return JsonResponse({'status': 'ignored', 'reason': 'not_main_branch'})
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        logger.error(f"Webhook error: {str(e)}")
        return JsonResponse({'error': 'Internal server error'}, status=500)
