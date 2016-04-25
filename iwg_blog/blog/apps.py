from django.apps import AppConfig

from watson import search as watson

from .adapters import ArticleAdapter


class BlogConfig(AppConfig):
    name = 'iwg_blog.blog'

    def ready(self):
        Article = self.get_model('Article')
        watson.register(Article, adapter_cls=ArticleAdapter)
