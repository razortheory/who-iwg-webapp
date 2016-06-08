from __future__ import absolute_import

from django.utils import timezone

from celery.schedules import crontab
from celery.task import periodic_task

from .models import Grantee


@periodic_task(run_every=crontab())
def publish_grantees():
    Grantee.objects.filter(status=Grantee.STATUS_READY_FOR_PUBLISH, published_at__lte=timezone.now()) \
        .update(status=Grantee.STATUS_PUBLISHED)
