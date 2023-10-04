import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")


app.conf.worker_concurrency = 4
app.conf.worker_prefork = True

app.autodiscover_tasks()

app.conf.task_acks_late = True


app.conf.beat_schedule = {
    "update-podcasts": {
        "task": "podcast.tasks.scrape_and_update_podcasts",
        "schedule": crontab(
            hour="3",
        ),
    },
}
