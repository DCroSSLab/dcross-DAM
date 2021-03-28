import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dcross_DAM.settings")

tasker = Celery('dcross_DAM')

tasker.config_from_object("django.conf:settings", namespace="CELERY")


# Pre-configured recurring tasks
tasker.conf.beat_schedule = {
    'earthquake_ncs': {
        'task': 'feed.tasks.earthquake_ncs',
        'schedule': crontab(minute="*/8")
    },
    'nowcast_imd': {
        'task': 'feed.tasks.nowcast_imd',
        'schedule': crontab(minute="*/10")
    },
    'weather_aws_arg': {
        'task': 'feed.tasks.weather_aws_arg',
        'schedule': crontab(minute="*/15")
    }
}

tasker.autodiscover_tasks()


@tasker.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
