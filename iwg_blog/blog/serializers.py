from iwg_blog.utils.serializers import JsonSerializer


class ArticleSerializer(JsonSerializer):
    serializable_fields = ['title', 'cover_image', 'short_description_text', 'published_at', 'get_absolute_url']

    def serialize_cover_image(self, value):
        return value.url
