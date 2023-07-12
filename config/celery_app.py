import os

from celery import Celery
from celery.schedules import crontab

# from attendance.tasks import calculate_attendance_task
# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("people_mate")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Schedule the task to run at 23:50 every day
app.conf.beat_schedule = {
    "calculate_attendance": {
        "task": "attendance.tasks.calculate_attendance_task",
        # 'schedule': crontab(minute=45, hour=23),
        "schedule": 70.0,
    },
}
