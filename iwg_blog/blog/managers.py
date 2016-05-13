from django.db import models
from django.db.models.functions import Lower

from ..utils.db import OrderableQuerySet


class CaseInsensitiveUniqueModelManagerMixin(object):
    insensitive_unique_fields = []

    def _filter_or_exclude(self, negate, *args, **kwargs):
        qs = self

        for field_name in self.insensitive_unique_fields:
            if field_name in kwargs:
                kwargs['%s__iexact' % field_name] = kwargs[field_name]
                del kwargs[field_name]

            for suffix in ['exact', 'startswith', 'endswith', 'regex', 'contains']:
                lookup = '__'.join([field_name, suffix])
                ilookup = '__'.join([field_name, 'i' + suffix])
                if lookup in kwargs:
                    kwargs[ilookup] = kwargs[lookup]
                    del kwargs[lookup]

            lookup = field_name + '__in'
            if lookup in kwargs:
                lower_field_name = field_name + '_lower'
                lower_lookup = lower_field_name + '__in'
                values = map(unicode.lower, kwargs[lookup])
                qs = qs.annotate(**{lower_field_name: Lower(field_name)})
                kwargs[lower_lookup] = values
                del kwargs[lookup]

        return super(CaseInsensitiveUniqueModelManagerMixin, qs)._filter_or_exclude(negate, *args, **kwargs)


class CaseInsensitiveUniqueModelManager(CaseInsensitiveUniqueModelManagerMixin, models.Manager):
    pass


class ArticleTagQuerySet(CaseInsensitiveUniqueModelManagerMixin, OrderableQuerySet):
    insensitive_unique_fields = ['name', ]

    def order_by_array(self, ordering_array, field_name=None, separator='\a'):
        qs = self

        if field_name in self.insensitive_unique_fields:
            lower_field_name = field_name + '_lower'
            qs = qs.annotate(**{lower_field_name: Lower(field_name)})

            ordering_array = map(unicode.lower, ordering_array)
            field_name = lower_field_name

        return super(ArticleTagQuerySet, qs).order_by_array(ordering_array, field_name, separator)


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
            .filter(status=self.model.STATUS_PUBLISHED)


class SampleArticleManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super(SampleArticleManager, self).get_queryset(*args, **kwargs).filter(is_sample=True)
