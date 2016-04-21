from __future__ import absolute_import

from datetime import timedelta

from celery.schedules import crontab
from celery.task import periodic_task

from django.conf import settings
from django.contrib.sites.models import Site
from django.utils import timezone

from mailing.shortcuts import render_send_email

from .models import Article, Subscriber


@periodic_task(run_every=crontab(day_of_week=1, hour=15), ignore_result=True)
def send_emails_for_subscribers():
    emails = Subscriber.objects.filter(send_email=True).values_list('email', flat=True)

    today = timezone.now()

    published_from = (today - timedelta(days=7)).replace(hour=0, minute=0, second=0)
    published_to = (today - timedelta(days=1)).replace(hour=23, minute=59, second=59)

    articles = Article.objects.filter(is_published=True,
                                      published_at__gte=published_from,
                                      published_at__lte=published_to)[:10]

    if not articles:
        return

    data = {'articles': articles,
            'domain': Site.objects.get_current(),
            'scheme': settings.META_SITE_PROTOCOL}

    batch_size = 20

    for offset in xrange(0, len(emails), batch_size):
        render_send_email(emails[offset:offset + batch_size], 'email/newsletter', data)
