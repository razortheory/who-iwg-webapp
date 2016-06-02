from django.db.models.expressions import Value, F
from django.db.models.functions import Concat, Lower

from iwg_blog.utils.db import Position


class OrderableQuerySetMixin(object):
    """
    Queryset mixin allowed to order by array index.
    """
    def order_by_array(self, ordering_array, field_name=None, separator='\a'):
        field_name = field_name or 'pk'
        return self.annotate(
            element_position=Position(
                Concat(Value(separator), F(field_name), Value(separator)),
                Value(separator + separator.join(map(str, ordering_array)) + separator),
            )
        ).order_by('element_position')


class CaseInsensitiveUniqueQuerysetMixin(object):
    """
    Case insensitive queryset. .filter(name='name') == .filter(name__iexact='name')
    """
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

        return super(CaseInsensitiveUniqueQuerysetMixin, qs)._filter_or_exclude(negate, *args, **kwargs)
