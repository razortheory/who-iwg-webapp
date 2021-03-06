from django.conf import settings

from .utils.watermarks import watermarks as watermarks_config


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
    """
    Watermark configs context processor.
    """
    context = {}
    for name, value in watermarks_config.items():
        context['watermark_%s' % name] = value
    return context


def social_links(request):
    return {
        'social_links': {
            'facebook': 'https://www.facebook.com/WHO',
            'twitter': 'https://twitter.com/who',
            'google_plus': 'https://plus.google.com/+who',
        }
    }
