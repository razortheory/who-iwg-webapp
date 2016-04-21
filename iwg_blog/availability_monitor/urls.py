from __future__ import absolute_import

from django.conf.urls import patterns, url

from .views import AvailabilityTestView


urlpatterns = \
    patterns('',
             url(r'^$', AvailabilityTestView.as_view(), name='availability-test'),
             )
