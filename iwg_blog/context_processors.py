from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static

from iwg_blog.blog.templatetags.blog_tags import absolute_url


def google_analytics(request):
    def ga_enabled():
        # if DEBUG
        if settings.DEBUG:
            return False

        # if there are no GA_CODE provided
        if not getattr(settings, 'GOOGLE_ANALYTICS_PROPERTY_ID', False):
            return False

        # allow to disable GA from settings via GA_ENABLED = False
        if hasattr(settings, 'GA_ENABLED'):
            return settings.GA_ENABLED
        return True

    context_ext = {
        "GA_ENABLED": ga_enabled(),
        "GA_CODE": getattr(settings, 'GOOGLE_ANALYTICS_PROPERTY_ID', ''),
    }
    return context_ext


def watermarks(request):
    return {
        'watermark_article': {
            'gravity': 'br',
            'width': '10%',
            'x': '2%',
            'y': '2%',
            'url': absolute_url(static('images/who-watermark.png')),
            'brightness_threshold': 200,
            'color': ['#ffffff', '#9b9b9b'],
            'opacity': 0.6,
        }
    }
