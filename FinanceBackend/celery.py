import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FinanceBackend.settings")
app = Celery("FinanceBackend")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


app.conf.update(
    broker_connection_retry_on_startup=True,
)


app.conf.beat_schedule = {
    "fetch_currency_data_daily": {
        "task": "api.tasks.fetch_currency_data",
        "schedule": crontab(hour=17, minute=34),  # Запуск каждый день в 10:00
    },
    "update_redis_hourly": {
        "task": "api.tasks.update_redis",
        "schedule": crontab(minute=35),  # Запуск каждый час
    },
}
