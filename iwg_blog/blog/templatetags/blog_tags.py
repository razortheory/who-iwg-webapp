from django import template
from django.conf import settings
from django.contrib.sites.models import Site

register = template.Library()


@register.simple_tag
def absolute_url(url):
    site = Site.objects.get_current()
    scheme = settings.META_SITE_PROTOCOL
    if '://' not in url:
        if url.startswith('/'):
            url = url[1:]
        return '%s://%s/%s' % (scheme, site, url)
    return url
