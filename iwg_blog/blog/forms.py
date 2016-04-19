from django import forms
from django.core.urlresolvers import reverse

from django_markdown.widgets import MarkdownWidget
from django_select2.forms import Select2MultipleWidget

from .widgets import ArticleContentMarkdownWidget


def set_attrs_for_field(field, attrs):
    field.widget.attrs = field.widget.attrs or {}
    field.widget.attrs.update(attrs)


class MarkdownFormField(forms.CharField):
    widget = MarkdownWidget

    def __init__(self, *args, **kwargs):
        # Using default form initialization to prevent dirty widget overriding
        super(MarkdownFormField, self).__init__(*args, **kwargs)


class ArticleAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ArticleAdminForm, self).__init__(*args, **kwargs)

        instance = kwargs.get('instance')
        if instance:
            preview_path = reverse('article_preview_view', args=[instance.id])
        else:
            preview_path = reverse('django_markdown_preview')

        markdown_attrs = {
            'data-upload-image-url': reverse('upload_image_ajax'),
            'data-preview-parser-url': preview_path,
        }
        set_attrs_for_field(self.fields['content'], markdown_attrs)
        set_attrs_for_field(self.fields['short_description'], markdown_attrs)
        self.fields['content'].widget.preview_path = preview_path

    class Meta:
        fields = forms.ALL_FIELDS
        widgets = {
            'tags': Select2MultipleWidget,
            'content': ArticleContentMarkdownWidget,
        }
        field_classes = {
            'content': MarkdownFormField,
        }
