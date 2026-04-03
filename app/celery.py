from celery import Celery
from celery.schedules import crontab

from app.core.config import settings


app = Celery(
    "tasks",
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    backend=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    include=["app.tasks.check_monitor", "app.tasks.restart_active_monitors", "app.tasks.cleanup"]
)


app.conf.beat_schedule = {
    "cleanup-old-checks": {
        "task": "app.tasks.cleanup.cleanup_old_checks_task",
        "schedule": crontab(hour=0, minute=0)
    }
}