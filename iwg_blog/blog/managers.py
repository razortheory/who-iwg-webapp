from django.db import models
from django.utils import timezone

from .queryset import ArticleTagQuerySet


class ArticleTagManager(models.Manager.from_queryset(ArticleTagQuerySet)):
    use_for_related_fields = True

    def get_queryset(self):
        queryset = super(ArticleTagManager, self).get_queryset()
        if hasattr(self, 'instance'):
            queryset = queryset.filter(**self.core_filters)
            queryset = queryset.order_by('%s.%s' % (self.through._meta.db_table, self.through._meta.pk.name))
        return queryset


class ArticleManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super(ArticleManager, self).get_queryset(*args, **kwargs).filter(is_sample=False)


class PublishedArticleManager(ArticleManager):
    def get_queryset(self, *args, **kwargs):
        return super(PublishedArticleManager, self).get_queryset(*args, **kwargs)\
            .filter(status=self.model.STATUS_PUBLISHED, published_at__lte=timezone.now())


class SampleArticleManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super(SampleArticleManager, self).get_queryset(*args, **kwargs).filter(is_sample=True)
