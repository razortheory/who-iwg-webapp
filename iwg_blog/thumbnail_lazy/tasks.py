from celery.task import task
from sorl.thumbnail import get_thumbnail


@task
def generate_thumbnail_lazy(*args, **kwargs):
    get_thumbnail(*args, **kwargs)
