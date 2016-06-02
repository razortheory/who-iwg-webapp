from django import forms
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models

from autoslug import AutoSlugField as RealAutoSlugField
from django_markdown.widgets import MarkdownWidget

from .widgets import TagitWidget


class MarkdownFormField(forms.CharField):
    widget = MarkdownWidget

    def __init__(self, *args, **kwargs):
        # Using default form initialization to prevent dirty widget overriding
        super(MarkdownFormField, self).__init__(*args, **kwargs)


class AutoSlugField(RealAutoSlugField):
    # XXX: Work around https://bitbucket.org/neithere/django-autoslug/issues/34/django-migrations-fail-if-autoslugfield
    def deconstruct(self):
        name, path, args, kwargs = super(AutoSlugField, self).deconstruct()
        if 'manager' in kwargs:
            del kwargs['manager']
        return name, path, args, kwargs


class OrderedModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def clean(self, value):
        qs = super(OrderedModelMultipleChoiceField, self).clean(value)
        qs = qs.order_by_array(value, field_name=self.to_field_name)
        return qs


class OrderedManyToManyField(models.ManyToManyField):
    def save_form_data(self, instance, data):
        m2m_model = getattr(instance, self.attname).through
        m2m_model.objects.filter(**{self.m2m_field_name(): instance}).delete()
        objects_to_create = [
            m2m_model(**{
                self.m2m_field_name(): instance,
                self.m2m_reverse_field_name(): related_instance
            }) for related_instance in data
        ]
        m2m_model.objects.bulk_create(objects_to_create)


class TagitField(OrderedModelMultipleChoiceField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', TagitWidget(autocomplete_url=reverse('blog:tags_autocomplete_ajax')))
        super(TagitField, self).__init__(*args, **kwargs)

    def _check_values(self, value):
        """
        Given a list of possible PK values, returns a QuerySet of the
        corresponding objects. Raises a ValidationError if a given value is
        invalid.
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
