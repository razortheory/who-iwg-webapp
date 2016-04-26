from django import forms

from autoslug import AutoSlugField as RealAutoSlugField
from django_markdown.widgets import MarkdownWidget


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
