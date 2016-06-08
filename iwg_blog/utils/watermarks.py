from django.contrib.staticfiles.templatetags.staticfiles import static

from .templatetags.tag_utils import absolute_url


watermark_article = {
    'gravity': 'br',
    'width': '10%',
    'x': '2h',
    'y': '2h',
    'url': absolute_url(static('blog/images/who-watermark.png')),
    'brightness_threshold': 200,
    'color': ['#ffffff', '#9b9b9b'],
    'opacity': 0.6,
}


# Watermarks to be passed to template context.
watermarks = {
    'article': watermark_article,
}
