import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')

app = Celery('conf')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'index-all-reviews-every-hour': {
        'task': 'apps.review.tasks.index_all_reviews',
        'schedule': 3600.0,
    },
    'index-all-reviews-every-minute': {
        'task': 'apps.review.tasks.index_latest_reviews',
        'schedule': 60.0,
    },
}