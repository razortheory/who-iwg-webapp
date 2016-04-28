from django.db import models

from ..utils.db import OrderableQuerySet


class CaseInsensitiveUniqueModelManagerMixin(object):
    insensitive_unique_fields = []

    def filter(self, **kwargs):
        for field_name in self.insensitive_unique_fields:
            if field_name in kwargs:
                kwargs['%s__iexact' % field_name] = kwargs[field_name]
                del kwargs[field_name]
        return super(CaseInsensitiveUniqueModelManagerMixin, self).filter(**kwargs)

    def get(self, **kwargs):
        for field_name in self.insensitive_unique_fields:
            if field_name in kwargs:
                kwargs['%s__iexact' % field_name] = kwargs[field_name]
                del kwargs[field_name]
        return super(CaseInsensitiveUniqueModelManagerMixin, self).get(**kwargs)


class CaseInsensitiveUniqueModelManager(CaseInsensitiveUniqueModelManagerMixin, models.Manager):
    pass


class ArticleTagManager(CaseInsensitiveUniqueModelManagerMixin, models.Manager.from_queryset(OrderableQuerySet)):
    insensitive_unique_fields = ['name', ]
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
            .filter(status=self.model.STATUS_PUBLISHED)


class SampleArticleManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super(SampleArticleManager, self).get_queryset(*args, **kwargs).filter(is_sample=True)
