from sorl.thumbnail import get_thumbnail

from ..utils.serializers import DictSerializer
from ..utils.watermarks import watermark_article


class ArticleSerializer(DictSerializer):
    serializable_fields = ['title', 'cover_image', 'short_description_text', 'published_at', 'get_absolute_url']

    def serialize_cover_image(self, value):
        return {
            'url': get_thumbnail(value, "1200", upscale=False, lazy=True, watermark=watermark_article).url,
            'thumb': get_thumbnail(value, "100x100", crop="center", lazy=True).url,
        }
