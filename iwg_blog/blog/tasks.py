from __future__ import absolute_import

from datetime import timedelta

from django.conf import settings
from django.contrib.sites.models import Site
from django.utils import timezone

from celery.schedules import crontab
from celery.task import periodic_task
from mailing.shortcuts import render_send_email

from . import watermarks_config
from .models import Article, Subscriber


@periodic_task(run_every=crontab(day_of_week=1, hour=15, minute=0), ignore_result=True)
def send_emails_for_subscribers():
    emails = Subscriber.objects.filter(send_email=True).values_list('email', flat=True)

    today = timezone.now()

    published_from = (today - timedelta(days=7)).replace(hour=0, minute=0, second=0)
    published_to = (today - timedelta(days=1)).replace(hour=23, minute=59, second=59)

    articles = Article.objects.filter(status=Article.STATUS_PUBLISHED,
                                      published_at__gte=published_from,
                                      published_at__lte=published_to)[:6]

    if not articles:
        return

    common_data = {
        'articles': articles,
        'domain': Site.objects.get_current(),
        'scheme': settings.META_SITE_PROTOCOL,
        'watermark_article': watermarks_config.watermark_article,
    }

    for email in emails:
        data = {'email': email}
        data.update(common_data)
        render_send_email([email, ], 'blog/email/newsletter', data)
