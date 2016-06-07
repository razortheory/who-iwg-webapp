from django import forms
from django_markdown.widgets import MarkdownWidget


class MarkdownFormField(forms.CharField):
    # Using default form initialization to prevent dirty widget overriding
    widget = MarkdownWidget


class OrderedModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    """ModelForm field; Keeping related objects ordering at saving"""
    def clean(self, value):
        qs = super(OrderedModelMultipleChoiceField, self).clean(value)
        qs = qs.order_by_array(value, field_name=self.to_field_name)
        return qs
