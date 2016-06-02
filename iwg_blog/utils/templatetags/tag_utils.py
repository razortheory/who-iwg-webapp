import re

from django import template
from django.conf import settings
from django.contrib.sites.models import Site

register = template.Library()


@register.simple_tag
def absolute_url(url):
    """
    Generate absolute url from provided.
    """

    if re.match(r'^(?:[a-z]+:)?//', url):
        return url

    site = Site.objects.get_current()
    scheme = settings.SITE_PROTOCOL

    if url.startswith('/'):
        url = url[1:]

    return '%s://%s/%s' % (scheme, site, url)
