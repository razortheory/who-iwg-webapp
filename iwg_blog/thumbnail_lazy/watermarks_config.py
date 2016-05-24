from django.contrib.staticfiles.templatetags.staticfiles import static

from ..blog.templatetags.blog_tags import absolute_url

watermark_article = {
    'gravity': 'br',
    'width': '10%',
    'x': '2%',
    'y': '2%',
    'url': absolute_url(static('blog/images/who-watermark.png')),
    'brightness_threshold': 200,
    'color': ['#ffffff', '#9b9b9b'],
    'opacity': 0.6,
}

watermarks = {
    'article': watermark_article,
}
