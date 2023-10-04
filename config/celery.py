import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")


app.conf.worker_concurrency = 4
app.conf.worker_prefork = True

app.autodiscover_tasks()

app.conf.task_acks_late = True
