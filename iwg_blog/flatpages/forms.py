from django import forms
from django.contrib.flatpages.forms import FlatpageForm

from ..blog.widgets import CustomMarkdownWidget
from ..utils.forms.mixins import AutoSaveModelFormMixin


class FlatPagesAdminForm(AutoSaveModelFormMixin, FlatpageForm):
    autosave_prefix = 'flatpages_flatpage'
    autosave_fields = ['content', ]

    class Meta:
        fields = forms.ALL_FIELDS
        widgets = {
            'content': CustomMarkdownWidget
        }
