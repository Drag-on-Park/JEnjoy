import os
from celery import Celery
from celery.schedules import crontab

# Django 프로젝트 설정을 로드
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Django 설정에서 Celery 관련 설정 가져오기
app.config_from_object('django.conf:settings', namespace='CELERY')

# Django의 모든 앱에서 tasks.py를 자동으로 검색
app.autodiscover_tasks()


# Celery Beat (주기적 작업) 사용
app.conf.beat_schedule = {
    'generate-daily-words-at-midnight': {
        'task': 'dictionary.tasks.generate_daily_words',
        'schedule': crontab(hour=00, minute=00),  # 초기 실행 (주기적 실행은 django-celery-beat에서 설정)
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')