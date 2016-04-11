from celery.task import periodic_task
from celery.schedules import timedelta


@periodic_task(run_every=timedelta(seconds=10))
def test_task():
    print('Celery works.')
