from django.db import models

from ..models import Category, Article, Tag


class CategoriesMixin(object):
    def get_context_data(self, **kwargs):
        context = dict()
        context['categories'] = Category.objects.all()[:8]
        context.update(kwargs)
        return super(CategoriesMixin, self).get_context_data(**context)


class FeaturedArticlesMixin(object):
    featured_articles_count = 5

    def get_context_data(self, **kwargs):
        context = dict()
        context['featured_articles'] = Article.published.filter(is_featured=True)[:self.featured_articles_count]
        context.update(kwargs)
        return super(FeaturedArticlesMixin, self).get_context_data(**context)


class TopArticlesMixin(object):
    top_articles_count = 3

    def get_context_data(self, **kwargs):
        context = dict()
        context['top_articles'] = Article.published.order_by('-hits')[:self.top_articles_count]
        context.update(kwargs)
        return super(TopArticlesMixin, self).get_context_data(**context)


class TopTagsMixin(object):
    top_tags_count = 20

    def get_context_data(self, **kwargs):
        context = dict()
        context['top_tags'] = Tag.objects.annotate(article_count=models.Count('articles')) \
            .order_by('-article_count')[:self.top_tags_count]
        context.update(kwargs)
        return super(TopTagsMixin, self).get_context_data(**context)
