from django import forms
from django.core.urlresolvers import reverse

from django_select2.forms import Select2MultipleWidget


def set_attrs_for_field(field, attrs):
    field.widget.attrs = field.widget.attrs or {}
    field.widget.attrs.update(attrs)


class ArticleAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ArticleAdminForm, self).__init__(*args, **kwargs)
        markdown_attrs = {
            'data-upload-image-url': reverse('upload_image_ajax'),
            'data-preview-parser-url': reverse('django_markdown_preview'),
        }
        set_attrs_for_field(self.fields['content'], markdown_attrs)
        set_attrs_for_field(self.fields['short_description'], markdown_attrs)

    class Meta:
        fields = forms.ALL_FIELDS
        widgets = {
            'tags': Select2MultipleWidget,
        }
