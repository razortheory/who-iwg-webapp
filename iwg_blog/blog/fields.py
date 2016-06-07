from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse

from ..utils.forms.fields import OrderedModelMultipleChoiceField
from ..utils.forms.widgets import TagitWidget


class TagitField(OrderedModelMultipleChoiceField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', TagitWidget(autocomplete_url=reverse('blog:tags_autocomplete_ajax')))
        super(TagitField, self).__init__(*args, **kwargs)

    def _check_values(self, value):
        """
        Given a list of possible PK values, returns a QuerySet of the
        corresponding objects. Raises a ValidationError if a given value is
        invalid.

        Equal to the default _check_values method except disabled invalid_choice validation
        and creating missing objects.
        """
        key = self.to_field_name or 'pk'
        # deduplicate given values to avoid creating many querysets or
        # requiring the database backend deduplicate efficiently.
        try:
            frozenset(value)
        except TypeError:
            # list of lists isn't hashable, for example
            raise ValidationError(
                self.error_messages['list'],
                code='list',
            )

        for pk in value:
            try:
                self.queryset.filter(**{key: pk})
            except (ValueError, TypeError):
                raise ValidationError(
                    self.error_messages['invalid_pk_value'],
                    code='invalid_pk_value',
                    params={'pk': pk},
                )

        qs = self.queryset.filter(**{key + '__in': value})

        existing_tags = map(unicode.lower, qs.values_list(key, flat=True))
        new_tags = []
        for v in value:
            if v.lower() in existing_tags:
                continue

            new_tags.append(self.queryset.model(**{key: v}))
        self.queryset.bulk_create(new_tags)

        return qs
