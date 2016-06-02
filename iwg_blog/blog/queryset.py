from django.db.models import QuerySet
from django.db.models.functions import Lower

from ..utils.queryset import CaseInsensitiveUniqueQuerysetMixin, OrderableQuerySetMixin


class ArticleTagQuerySet(CaseInsensitiveUniqueQuerysetMixin, OrderableQuerySetMixin, QuerySet):
    insensitive_unique_fields = ['name', ]

    def order_by_array(self, ordering_array, field_name=None, separator='\a'):
        qs = self

        if field_name in self.insensitive_unique_fields:
            lower_field_name = field_name + '_lower'
            qs = qs.annotate(**{lower_field_name: Lower(field_name)})

            ordering_array = map(unicode.lower, ordering_array)
            field_name = lower_field_name

        return super(ArticleTagQuerySet, qs).order_by_array(ordering_array, field_name, separator)
