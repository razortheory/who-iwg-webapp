from watson.search import SearchAdapter


class ArticleAdapter(SearchAdapter):
    def get_title(self, obj):
        return obj.title

    def get_description(self, obj):
        return obj.short_description_text

    def get_content(self, obj):
        return obj.content_text
